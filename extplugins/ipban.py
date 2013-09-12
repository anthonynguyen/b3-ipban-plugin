# IP Ban Plugin for B3
# By clearskies (Anthony Nguyen)
# GPL licensed

import b3
import b3.events
import b3.plugin
import re
import types

__version__ = "2"
__author__ = "clearskies (Anthony Nguyen)"

class IpbanPlugin(b3.plugin.Plugin):
	requiresConfigFile = False
	maxFromIP = 3

	ipRegex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
	rangeRegex = r"(\d{1,3}|\*)\.(\d{1,3}|\*)\.(\d{1,3}|\*)\.(\d{1,3}|\*)"

	def onStartup(self):
		self._admin = self.console.getPlugin("admin")
		self._admin.registerCommand(self, "ipban", 100, self.cmd_ipban, "ipb")
		self._admin.registerCommand(self, "ipunban", 100, self.cmd_ipunban, "ipu")

		self.registerEvent(b3.events.EVT_CLIENT_CONNECT)

		def ban(self, client, reason='', admin=None, silent=False, *kwargs):
			q = "INSERT INTO `ipbans` (`client_id`, `ip`) VALUES ('{0}', '{1}');".format(client.id, client.ip)
			try:
				self.storage.query(q)
			except IntegrityError:
				pass
			self.oban(client, reason, admin, silent, *kwargs)

		def unban(self, client, reason='', admin=None, silent=False, *kwargs):
			q = "DELETE FROM `ipbans` WHERE `client_id` = '{0}';".format(client.id)
			self.storage.query(q)
			self.ounban(client, reason, admin, silent, *kwargs)

		self.console.oban = self.console.ban
		self.console.ban = ban
		self.console.ban = types.MethodType(ban, self.console)

		self.console.ounban = self.console.unban
		self.console.unban = unban
		self.console.unban = types.MethodType(unban, self.console)

		self.rangeCache = []
		q = "SELECT * FROM `iprangebans`;"
		c = self.console.storage.query(q)
		if c.rowcount > 0:
			while not c.EOF:
				r = c.getRow()
				self.rangeCache.append(r["range"])
				c.moveNext()
		c.close()

	def onEvent(self, event):
		if event.type == b3.events.EVT_CLIENT_CONNECT:
			q = "SELECT * FROM `ipbans` WHERE `ip` = '{0}';".format(event.client.ip)
			c = self.console.storage.query(q)
			if c.rowcount > 0:
				self.console.write("kick {0}".format(event.client.cid))
			c.close()

			if self.maxFromIP > 0:
				curOn = []
				for c in self.console.clients.getList():
					if c.ip == event.client.ip:
						curOn.append(c)
				if len(curOn) > self.maxFromIP:
					for c in curOn:
						self.console.write("kick {0}".format(c.cid))

			parts = event.client.ip.split(".")
			for ipRange in [r.split(".") for r in self.rangeCache]:
				blockMatches = 0
				for clientBlock, bannedBlock in zip(parts, ipRange):
					if bannedBlock == "*" or clientBlock == bannedBlock:
						blockMatches += 1
				if blockMatches == 4:
					self.console.write("kick {0}".format(event.client.cid))
					break

	def cmd_ipban(self, data, client, cmd = None):
		"""
		<ip/range> - Bans an IP address or an address range.
		"""
		if re.match(self.ipRegex, data):
			try:
				q = "INSERT INTO `ipbans` (`client_id`, `ip`) VALUES ('{0}', '{1}');".format(0, data)
				self.console.storage.query(q)
				client.message("^2{0}^7 added to IP ban database.".format(data))
			except:
				client.message("^2{0}^7 already in IP ban database.".format(data))
		elif re.match(self.rangeRegex, data):
			try:
				q = "INSERT INTO `iprangebans` (`range`) VALUES ('{0}');".format(data)
				self.console.storage.query(q)
				self.rangeCache.append(data)
				client.message("^2{0}^7 added to IP range ban database.".format(data))
			except:
				client.message("^2{0}^7 already in IP ban database.".format(data))
		else:
			client.message("That's not a valid IP address or address range.")

	def cmd_ipunban(self, data, client, cmd = None):
		"""
		<ip/range> - Unbans an IP address or an address range.
		"""
		if re.match(self.ipRegex, data):
			q = "SELECT * FROM `ipbans` WHERE `ip` = '{0}';".format(data)
			c = self.console.storage.query(q)
			if c.rowcount == 0:
				client.message("^2{0}^7 is not in the IP ban database.".format(data))
				return
			c.close()

			q = "DELETE FROM `ipbans` WHERE `ip` = '{0}';".format(data)
			self.console.storage.query(q)
			client.message("^2{0}^7 removed from IP ban database.".format(data))
		elif re.match(self.rangeRegex, data):
			if data not in self.rangeCache:
				client.message("^2{0}^7 is not in the IP range ban database.".format(data))
				return

			q = "DELETE FROM `iprangebans` WHERE `range` = '{0}';".format(data)
			self.console.storage.query(q)
			client.message("^2{0}^7 removed from IP range ban database.".format(data))
		else:
			client.message("That's not a valid IP address or address range.")