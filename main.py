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
		self.redirect('/keyinproduct')
		
class PurchaseUploadHandler(webapp2.RequestHandler):
	def post(self):
		upload_item = self.request.get('Product_item')
		upload_amount = self.request.get('Product_amount')
		upload_total = self.request.get('product_total')
		upload_moneyin = self.request.get('checkbox_money')
		upload_sold = self.request.get('checkbox_sold')
		upload_buyer = self.request.get('product_buyer')
		
		self.response.out.write(upload_item+"<br>"+upload_amount+"<br>"+upload_total+"<br>"+upload_buyer+"<br>")
		
		var b_upload_moneyin = false;
		var b_upload_sold = false;
		if (upload_moneyin == "on"):
			b_upload_moneyin = true;
		if (upload_sold == "on"):
			b_upload_sold = true;
		
		product = ItemData(item=upload_item, amount=int(upload_amount), total=int(upload_total), moneyin=b_upload_moneyin, sold=b_upload_sold, buyer=upload_buyer)
		product.put()
		self.redirect('/')
		

class MainHandler(webapp2.RequestHandler):
    def get(self):
		
		self.response.out.write('<html><body><script type="text/javascript">\n')
		self.response.out.write('var single_price = 0;\nvar ProductList = {};\n')
		
		products = ItemData.query().order(ItemData.item)
		for product in products:
			self.response.out.write('ProductList["%s"] = ' %(product.item))
			self.response.out.write('"data:image/png;base64,"+"%s";' %b64encode(product.pic))
			self.response.out.write('ProductList["%s"+"_price"] = ' %(product.item))
			self.response.out.write('"%s";' %(product.price))
		self.response.write('''
							   function onSelectedFunc(onSelectedValue) {
								   document.getElementById("showimg").src=ProductList[onSelectedValue.value];
								   document.getElementById("product_price").textContent="Price: "+ProductList[onSelectedValue.value+"_price"];
								   single_price = parseInt(ProductList[onSelectedValue.value+"_price"]);
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
								   var cost = parseInt(onSelectedAmount.value) * single_price;
								   document.getElementById("upload_total").value = cost.toString();
							   }
							   </script>''')
		self.response.out.write('<form action="/upload_purchase" method="POST" enctype="multipart/form-data" onsubmit="return checkFile()"><select name="Product_item" id="upload_item" onChange="onSelectedFunc(this)"><option value="" selected disabled hidden>Choose here</option>')
		
		for product in products:	
			self.response.out.write('<option value="%s">%s</option>' %(product.item, product.item))
		
		self.response.out.write('</select><br><img id="showimg" height="100"><div id="product_price"></div>')
		self.response.out.write('Product Amount: <select name="Product_amount" id="upload_amount" onChange="totalChangedFunc(this)"><option value="" selected disabled hidden>Choose here</option>')
		for x in range(1,11):
			self.response.out.write('<option value="%s">%s</option>' %(str(x),str(x)))
		
		self.response.out.write("""</select><br>
			Total: <input type="text" name="product_total" id="upload_total"><br>
			<input type="checkbox" name="checkbox_money">money in<br>
			<input type="checkbox" name="checkbox_sold">sold<br>
			Buyer: <input type="text" name="product_buyer" id="upload_buyer"><br>
			<input type="submit" name="submit" value="Submit"> </form></body></html>""")
		

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/keyinproduct', ItemUploadFormHandler),
	('/upload_item', ItemUploadHandler),
	('/upload_purchase', PurchaseUploadHandler)
], debug=True)
