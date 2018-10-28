#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import ndb
from base64 import b64encode

Mode = "None"

class ItemData(ndb.Model):
	item = ndb.StringProperty()
	price = ndb.IntegerProperty()
	pic = ndb.BlobProperty()
	

class PurchaseData(ndb.Model):
	item = ndb.StringProperty()
	amount = ndb.IntegerProperty()
	total = ndb.IntegerProperty()
	moneyin = ndb.BooleanProperty()
	sold = ndb.BooleanProperty()
	buyer = ndb.StringProperty()
	note = ndb.StringProperty()
	
class ItemUploadFormHandler(webapp2.RequestHandler):
	def get(self):
		
		self.response.out.write('<html><body>')
		self.response.write('''<script type="text/javascript">
							   function checkFile() {
								   var fileElement = document.getElementById("upload_file");
								   var fileElement1 = document.getElementById("upload_name");
								   var fileElement2 = document.getElementById("upload_price");
								   if (fileElement.value != "" && fileElement1.value != "" && fileElement2.value != "") {
									   alert("File upload success!");
									   return true;
								   } else {
									   alert("You must select a file or enter a name to upload!");
									   return false;
								   }
							   }
							   </script>''')
		self.response.out.write('<form action="/upload_item" method="POST" enctype="multipart/form-data" onsubmit="return checkFile()">')
		self.response.out.write("""Product Name: <input type="text" name="product_name" id="upload_name"><br>
			Product Price: <input type="text" name="product_price" id="upload_price"><br>
			Upload Product Photo: <input type="file" name="file" id="upload_file"><br> 
			<input type="submit" name="submit" value="Submit"> </form></body></html>""")
			
class ItemUploadHandler(webapp2.RequestHandler):
	def post(self):
		upload_file = self.request.get('file')
		upload_name = self.request.get('product_name')
		upload_price = self.request.get('product_price')
		product = ItemData(item=upload_name, price=int(upload_price), pic=upload_file)
		product.put()
		#self.redirect('/keyinproduct')
		#self.response.out.write('<meta http-equiv="refresh" content="0.1; url=http://localhost:8080/keyinproduct" />')
		self.response.out.write('<meta http-equiv="refresh" content="0.1; url=http://one-to-beauty.appspot.com/keyinproduct" />')
		
class PurchaseUploadHandler(webapp2.RequestHandler):
	def post(self):
		upload_item = self.request.get('Product_item')
		upload_amount = self.request.get('Product_amount')
		upload_total = self.request.get('product_total')
		upload_moneyin = self.request.get('checkbox_money')
		upload_sold = self.request.get('checkbox_sold')
		upload_buyer = self.request.get('product_buyer')
		upload_note = self.request.get('product_note')
		
		
		b_upload_moneyin = False;
		b_upload_sold = False;
		if (upload_moneyin == "on"):
			b_upload_moneyin = True;
		if (upload_sold == "on"):
			b_upload_sold = True;
		
		product = PurchaseData(item=upload_item, amount=int(upload_amount), total=int(upload_total), moneyin=b_upload_moneyin, sold=b_upload_sold, buyer=upload_buyer, note=upload_note)
		product.put()
		#self.redirect('/')
		#self.response.out.write('<meta http-equiv="refresh" content="0.1; url=http://localhost:8080/" />')
		self.response.out.write('<meta http-equiv="refresh" content="0.1; url=http://one-to-beauty.appspot.com/" />')
		
class PurchaseModifyHandler(webapp2.RequestHandler):
	def post(self):
		modify_submit = self.request.get('modify_submit')
		if modify_submit == 'Modify':
			modify_id = self.request.get('modify_id')
			modify_item_id = self.request.get('modify_item_id')
			modify_buyer = self.request.get('modify_buyer')
			modify_item = self.request.get('modify_item')
			modify_amount = self.request.get('modify_amount')
			modify_total = self.request.get('modify_total')
			modify_moneyin = self.request.get('modify_moneyin')
			modify_sold = self.request.get('modify_sold')
			modify_note = self.request.get('modify_note')
			
			
			b_modify_moneyin = False;
			b_modify_sold = False;
			if (modify_moneyin == "on"):
				b_modify_moneyin = True;
			if (modify_sold == "on"):
				b_modify_sold = True;
			
			modify_purchase = PurchaseData.query(ancestor=ndb.Key(PurchaseData, int(modify_id))).get()
			modify_purchase.buyer = modify_buyer
			modify_purchase.item = modify_item_id
			modify_purchase.amount = int(modify_amount)
			modify_purchase.total = int(modify_total)
			modify_purchase.moneyin = b_modify_moneyin
			modify_purchase.sold = b_modify_sold
			modify_purchase.note = modify_note
			
			modify_purchase.put()
		
		
		elif modify_submit == 'Delete':
			modify_id = self.request.get('modify_id')
			modify_purchase = PurchaseData.query(ancestor=ndb.Key(PurchaseData, int(modify_id))).get()
			modify_purchase.key.delete()
		
		
		#self.redirect('/')
		#self.response.out.write('<meta http-equiv="refresh" content="0.1; url=http://localhost:8080/" />')
		self.response.out.write('<meta http-equiv="refresh" content="0.1; url=http://one-to-beauty.appspot.com/" />')
		

class MainHandler(webapp2.RequestHandler):
	def post(self):
		if (self.request.get('mode')):
			Mode = self.request.get('mode')
			#self.response.out.write(Mode)
		
		self.response.out.write("""<html><style>
			#container {
			  height: 100%;
			  width: 100%;
			  display: flex;
			}
			#output_form {
			  width: 70%;
			  float: left;
			}
			#input_form {
			  width: 30%;
			  float: right;
			  padding: 10px;
			  background-color: white;
			}
			table {
				font-family: arial, sans-serif;
				border-collapse: collapse;
			}

			td, th {
				border: 1px solid #dddddd;
				text-align: center;
				padding: 5px;
			}

			tr:nth-child(even) {
				background-color: #dddddd;
			}
		</style><body><div id="container"><div id="output_form"><table><br>""")
		
		if Mode == 'None':
			purchases = PurchaseData.query().order(PurchaseData.key)
		elif Mode == 'Buyer':
			purchases = PurchaseData.query().order(PurchaseData.buyer).order(PurchaseData.item)
		elif Mode == 'Item':
			purchases = PurchaseData.query().order(PurchaseData.item).order(-PurchaseData.amount)
		elif Mode == 'MoneyIn':
			purchases = PurchaseData.query().order(PurchaseData.moneyin).order(PurchaseData.sold)
		
		products = ItemData.query().order(ItemData.item)
		self.response.out.write('<tr><form action="/" method="POST" enctype="multipart/form-data">')
		self.response.out.write('<th><input type="submit" name="mode" value="Buyer"></th>')
		self.response.out.write('<th><input type="submit" name="mode" value="Item"></th>')
		self.response.out.write('<th>Amount</th><th>Total</th>')
		self.response.out.write('<th><input type="submit" name="mode" value="MoneyIn"></th>')
		self.response.out.write('<th>Export</th>')
		self.response.out.write('<th>Note</th><th>Modify</th><th>Delete</th></form></tr>')
		for purchase in purchases:
			self.response.out.write('<tr><form action="/modify_purchase" method="POST" enctype="multipart/form-data">')
			self.response.out.write("<input type='hidden' name='modify_id' value='%s'>" %(purchase.key.id()))
			self.response.out.write("<input type='hidden' name='modify_item_id' value='%s'>" %(purchase.item))
			self.response.out.write('<td><input type="text" name="modify_buyer" value="%s" size="10"></td>' %(purchase.buyer))
			
			
			self.response.out.write('<td><select style="width:100px;" name="modify_item" id="modify_item_%s" onChange="onSelectedFunc1(this)">' %(purchase.key.id()))
			for product in products:	
				if int(purchase.item) == product.key.id():
					self.response.out.write('<option value="%s" selected>%s</option>' %(product.key.id(), product.item))
				else:
					self.response.out.write('<option value="%s">%s</option>' %(product.key.id(), product.item))
			#self.response.out.write('<td><input type="text" name="modify_item" value="%s"></td>' %(ItemData.query(ancestor=ndb.Key(ItemData, int(purchase.item))).get().item))
			self.response.out.write('</select></td>')
			
			self.response.out.write('<td><select name="modify_amount" id="modify_amount_%s" onChange="totalChangedFunc1(this)">' %(purchase.key.id()))
			for x in range(1,11):
				if int(purchase.amount) == x:
					self.response.out.write('<option value="%s" selected>%s</option>' %(str(x),str(x)))
				else:
					self.response.out.write('<option value="%s">%s</option>' %(str(x),str(x)))
			#self.response.out.write('<td><input type="text" name="modify_amount" value="%s"></td>' %(purchase.amount))
			self.response.out.write('</select></td>')
			
			
			self.response.out.write('<td><input type="text" id="modify_total_%s" name="modify_total" value="%s" size="3"></td>' %(purchase.key.id(), purchase.total))
			if purchase.moneyin:
				self.response.out.write('<td><input type="checkbox" name="modify_moneyin" checked></td>')
			else:
				self.response.out.write('<td><input type="checkbox" name="modify_moneyin"></td>')
			if purchase.sold:
				self.response.out.write('<td><input type="checkbox" name="modify_sold" checked></td>')
			else:
				self.response.out.write('<td><input type="checkbox" name="modify_sold"></td>')
				
			self.response.out.write('<td><input type="text" name="modify_note" value="%s" size="3"></td>' %(purchase.note))
			self.response.out.write('<td><input type="submit" name="modify_submit" value="Modify"></td>')
			self.response.out.write('<td><input type="submit" name="modify_submit" value="Delete"></td>')
			self.response.out.write('</form></tr><br>')
			
			
		self.response.out.write('</table></div>')
		self.response.out.write('<div id="input_form"><form action="/upload_purchase" method="POST" enctype="multipart/form-data" onsubmit="return checkFile()"><select style="width:100px;" name="Product_item" id="upload_item" onChange="onSelectedFunc(this)"><option value="" selected disabled hidden>Choose here</option>')
		
		for product in products:	
			self.response.out.write('<option value="%s">%s</option>' %(product.key.id(), product.item))
		
		self.response.out.write('</select><br><img id="showimg" height="100"><div id="product_price"></div>')
		self.response.out.write('Product Amount: <select name="Product_amount" id="upload_amount" onChange="totalChangedFunc(this)"><option value="" selected disabled hidden>Choose here</option>')
		for x in range(1,11):
			self.response.out.write('<option value="%s">%s</option>' %(str(x),str(x)))
		
		self.response.out.write("""</select><br>
			Total: <input type="text" name="product_total" id="upload_total"><br>
			<input type="checkbox" name="checkbox_money">money in<br>
			<input type="checkbox" name="checkbox_sold">sold<br>
			Buyer: <input type="text" name="product_buyer" id="upload_buyer"><br>
			Note: <input type="text" name="product_note"><br>
			<input type="submit" name="submit" value="Submit"> </form></div>""")
		
		self.response.out.write("""<script type="text/javascript">\n""")
		self.response.out.write('var single_price = 0;\nvar amount = 0;\nvar ProductList = {};\n')
		
		
		for product in products:
			self.response.out.write('ProductList["%s"] = ' %(product.key.id()))
			self.response.out.write('"data:image/png;base64,"+"%s";' %b64encode(product.pic))
			self.response.out.write('ProductList["%s"+"_price"] = ' %(product.key.id()))
			self.response.out.write('"%s";' %(product.price))
		self.response.write('''
							   function onSelectedFunc(onSelectedValue) {
								   document.getElementById("showimg").src=ProductList[onSelectedValue.value];
								   document.getElementById("product_price").textContent="Price: "+ProductList[onSelectedValue.value+"_price"];
								   single_price = parseInt(ProductList[onSelectedValue.value+"_price"]);
								   if (amount>0){
									var cost = amount * single_price;
									document.getElementById("upload_total").value = cost.toString();
								   }
							   }
							   function onSelectedFunc1(onSelectedValue) {
								   var modify_form_id = onSelectedValue.id.split("item_")[1];
								   var single_price1 = parseInt(ProductList[onSelectedValue.value+"_price"]);
								   var amount_getid = document.getElementById("modify_amount_"+modify_form_id);
								   var amount1 = parseInt(amount_getid.options[amount_getid.selectedIndex].value);
								   var cost = amount1 * single_price1;
								   document.getElementById("modify_total_"+modify_form_id).value = cost.toString();
							   }
							   function checkFile() {
								   var fileElement = document.getElementById("upload_item");
								   var fileElement1 = document.getElementById("upload_amount");
								   var fileElement2 = document.getElementById("upload_total");
								   var fileElement3 = document.getElementById("upload_buyer");
								   if (fileElement.value != "" && fileElement1.value != "" && fileElement2.value != "" && fileElement3.value != "") {
									   alert("File upload success!");
									   return true;
								   } else {
									   alert("You must select a file or enter a name to upload!");
									   return false;
								   }
							   }
							   function totalChangedFunc(onSelectedAmount){
								   amount = parseInt(onSelectedAmount.value);
								   var cost = amount * single_price;
								   document.getElementById("upload_total").value = cost.toString();
							   }
							   function totalChangedFunc1(onSelectedAmount){
								   var modify_form_id = onSelectedAmount.id.split("amount_")[1];
								   var amount1 = parseInt(onSelectedAmount.value);
								   var item_getid = document.getElementById("modify_item_"+modify_form_id);
								   var single_price1 = parseInt(ProductList[item_getid.options[item_getid.selectedIndex].value+"_price"]);
								   var cost = amount1 * single_price1;
								   document.getElementById("modify_total_"+modify_form_id).value = cost.toString();
							   }
							   </script></body></html>''')
	def get(self):
		self.response.out.write("""<html><style>
			#container {
			  height: 100%;
			  width: 100%;
			  display: flex;
			}
			#output_form {
			  width: 70%;
			}
			#input_form {
			  width: 30%;
			  float: right;
			  padding: 10px;
			  background-color: white;
			}
			table {
				font-family: arial, sans-serif;
				border-collapse: collapse;
			}

			td, th {
				border: 1px solid #dddddd;
				text-align: center;
				padding: 5px;
			}

			tr:nth-child(even) {
				background-color: #dddddd;
			}
		</style><body><div id="container"><div id="output_form"><table><br>""")
		
		purchases = PurchaseData.query().order(PurchaseData.key)
		
		products = ItemData.query().order(ItemData.item)
		self.response.out.write('<tr><form action="/" method="POST" enctype="multipart/form-data">')
		self.response.out.write('<th><input type="submit" name="mode" value="Buyer"></th>')
		self.response.out.write('<th><input type="submit" name="mode" value="Item"></th>')
		self.response.out.write('<th>Amount</th><th>Total</th>')
		self.response.out.write('<th><input type="submit" name="mode" value="MoneyIn"></th>')
		self.response.out.write('<th><input type="submit" name="mode" value="Export"></th>')
		self.response.out.write('<th>Note</th><th>Modify</th><th>Delete</th></form></tr>')
		for purchase in purchases:
			self.response.out.write('<tr><form action="/modify_purchase" method="POST" enctype="multipart/form-data">')
			self.response.out.write("<input type='hidden' name='modify_id' value='%s'>" %(purchase.key.id()))
			self.response.out.write("<input type='hidden' name='modify_item_id' value='%s'>" %(purchase.item))
			self.response.out.write('<td><input type="text" name="modify_buyer" value="%s" size="3"></td>' %(purchase.buyer))
			
			
			self.response.out.write('<td><select style="width:100px;" name="modify_item" id="modify_item_%s" onChange="onSelectedFunc1(this)">' %(purchase.key.id()))
			for product in products:	
				if int(purchase.item) == product.key.id():
					self.response.out.write('<option value="%s" selected>%s</option>' %(product.key.id(), product.item))
				else:
					self.response.out.write('<option value="%s">%s</option>' %(product.key.id(), product.item))
			#self.response.out.write('<td><input type="text" name="modify_item" value="%s"></td>' %(ItemData.query(ancestor=ndb.Key(ItemData, int(purchase.item))).get().item))
			self.response.out.write('</select></td>')
			
			self.response.out.write('<td><select name="modify_amount" id="modify_amount_%s" onChange="totalChangedFunc1(this)">' %(purchase.key.id()))
			for x in range(1,11):
				if int(purchase.amount) == x:
					self.response.out.write('<option value="%s" selected>%s</option>' %(str(x),str(x)))
				else:
					self.response.out.write('<option value="%s">%s</option>' %(str(x),str(x)))
			#self.response.out.write('<td><input type="text" name="modify_amount" value="%s"></td>' %(purchase.amount))
			self.response.out.write('</select></td>')
			
			
			self.response.out.write('<td><input type="text" id="modify_total_%s" name="modify_total" value="%s" size="3"></td>' %(purchase.key.id(), purchase.total))
			if purchase.moneyin:
				self.response.out.write('<td><input type="checkbox" name="modify_moneyin" checked></td>')
			else:
				self.response.out.write('<td><input type="checkbox" name="modify_moneyin"></td>')
			if purchase.sold:
				self.response.out.write('<td><input type="checkbox" name="modify_sold" checked></td>')
			else:
				self.response.out.write('<td><input type="checkbox" name="modify_sold"></td>')
				
			self.response.out.write('<td><input type="text" name="modify_note" value="%s" size="3"></td>' %(purchase.note))
			self.response.out.write('<td><input type="submit" name="modify_submit" value="Modify"></td>')
			self.response.out.write('<td><input type="submit" name="modify_submit" value="Delete"></td>')
			self.response.out.write('</form></tr><br>')
			
			
		self.response.out.write('</table></div>')
		self.response.out.write('<div id="input_form"><form action="/upload_purchase" method="POST" enctype="multipart/form-data" onsubmit="return checkFile()"><select style="width:100px;" name="Product_item" id="upload_item" onChange="onSelectedFunc(this)"><option value="" selected disabled hidden>Choose here</option>')
		
		for product in products:	
			self.response.out.write('<option value="%s">%s</option>' %(product.key.id(), product.item))
		
		self.response.out.write('</select><br><img id="showimg" height="100"><div id="product_price"></div>')
		self.response.out.write('Product Amount: <select name="Product_amount" id="upload_amount" onChange="totalChangedFunc(this)"><option value="" selected disabled hidden>Choose here</option>')
		for x in range(1,11):
			self.response.out.write('<option value="%s">%s</option>' %(str(x),str(x)))
		
		self.response.out.write("""</select><br>
			Total: <input type="text" name="product_total" id="upload_total"><br>
			<input type="checkbox" name="checkbox_money">money in<br>
			<input type="checkbox" name="checkbox_sold">sold<br>
			Buyer: <input type="text" name="product_buyer" id="upload_buyer"><br>
			Note: <input type="text" name="product_note"><br>
			<input type="submit" name="submit" value="Submit"> </form></div>""")
		
		self.response.out.write("""<script type="text/javascript">\n""")
		self.response.out.write('var single_price = 0;\nvar amount = 0;\nvar ProductList = {};\n')
		
		
		for product in products:
			self.response.out.write('ProductList["%s"] = ' %(product.key.id()))
			self.response.out.write('"data:image/png;base64,"+"%s";' %b64encode(product.pic))
			self.response.out.write('ProductList["%s"+"_price"] = ' %(product.key.id()))
			self.response.out.write('"%s";' %(product.price))
		self.response.write('''
							   function onSelectedFunc(onSelectedValue) {
								   document.getElementById("showimg").src=ProductList[onSelectedValue.value];
								   document.getElementById("product_price").textContent="Price: "+ProductList[onSelectedValue.value+"_price"];
								   single_price = parseInt(ProductList[onSelectedValue.value+"_price"]);
								   if (amount>0){
									var cost = amount * single_price;
									document.getElementById("upload_total").value = cost.toString();
								   }
							   }
							   function onSelectedFunc1(onSelectedValue) {
								   var modify_form_id = onSelectedValue.id.split("item_")[1];
								   var single_price1 = parseInt(ProductList[onSelectedValue.value+"_price"]);
								   var amount_getid = document.getElementById("modify_amount_"+modify_form_id);
								   var amount1 = parseInt(amount_getid.options[amount_getid.selectedIndex].value);
								   var cost = amount1 * single_price1;
								   document.getElementById("modify_total_"+modify_form_id).value = cost.toString();
							   }
							   function checkFile() {
								   var fileElement = document.getElementById("upload_item");
								   var fileElement1 = document.getElementById("upload_amount");
								   var fileElement2 = document.getElementById("upload_total");
								   var fileElement3 = document.getElementById("upload_buyer");
								   if (fileElement.value != "" && fileElement1.value != "" && fileElement2.value != "" && fileElement3.value != "") {
									   alert("File upload success!");
									   return true;
								   } else {
									   alert("You must select a file or enter a name to upload!");
									   return false;
								   }
							   }
							   function totalChangedFunc(onSelectedAmount){
								   amount = parseInt(onSelectedAmount.value);
								   var cost = amount * single_price;
								   document.getElementById("upload_total").value = cost.toString();
							   }
							   function totalChangedFunc1(onSelectedAmount){
								   var modify_form_id = onSelectedAmount.id.split("amount_")[1];
								   var amount1 = parseInt(onSelectedAmount.value);
								   var item_getid = document.getElementById("modify_item_"+modify_form_id);
								   var single_price1 = parseInt(ProductList[item_getid.options[item_getid.selectedIndex].value+"_price"]);
								   var cost = amount1 * single_price1;
								   document.getElementById("modify_total_"+modify_form_id).value = cost.toString();
							   }
							   </script></body></html>''')
		
		

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/keyinproduct', ItemUploadFormHandler),
	('/upload_item', ItemUploadHandler),
	('/upload_purchase', PurchaseUploadHandler),
	('/modify_purchase', PurchaseModifyHandler)
], debug=True)
