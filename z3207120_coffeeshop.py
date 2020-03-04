import rdflib
from rdflib import Namespace
from rdflib import Literal

########################################
# 9322 ASSIGNMENT 2 DAN KENNEDY z3207120
########################################

owlNS = Namespace("http://www.w3.org/2002/07/owl#")
owlClass = owlNS["Class"]
owlObjectProperty = owlNS["ObjectProperty"]
owlDatatypeProperty = owlNS["DatatypeProperty"]
rdfNS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfProperty = rdfNS["Property"]
rdfType = rdfNS["type"]
rdfsNS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
rdfsSubClassOf = rdfsNS["subClassOf"]
rdfsDomain = rdfsNS["domain"]
rdfsRange = rdfsNS["range"]
rdfsLabel = rdfsNS["label"]

# XML properties
xsdNS = Namespace("http://www.w3.org/2001/XMLSchema#")
xsdString = xsdNS["string"] #xsd:string
xsdDateTime = xsdNS["dateTime"] #xsd:dateTime
xsdInteger = xsdNS["integer"] #xsd:integer
xsdDecimal = xsdNS["decimal"] #xsd:decimal

coffeeNS = Namespace("http://www.z3207120.unsw.edu.au/ontology#")

# Class names
productClass = coffeeNS['Product']
orderClass = coffeeNS['Order']
additionClass = coffeeNS['Addition']
coffeeClass = coffeeNS['Coffee']
statusClass = coffeeNS['Status']
personClass = coffeeNS['Person']
customerClass = coffeeNS['Customer']
employeeClass = coffeeNS['Employee']
paymentClass = coffeeNS['Payment']

# Property names
orderIncludesProduct = coffeeNS['orderIncludesProduct']
hasStatus = coffeeNS['hasStatus']
orderedBy = coffeeNS['orderedBy']
paymentAssociatedWith = coffeeNS['paymentAssociatedWith']

# Datatype properties
orderId = coffeeNS['orderId']
orderTime = coffeeNS['orderTime']
orderStatus = coffeeNS['orderStatus']
employeeRole = coffeeNS['employeeRole']
fullName = coffeeNS['fullName']
customerId = coffeeNS['customerId']
employeeId = coffeeNS['employeeId']
paymentType = coffeeNS['paymentType']
price = coffeeNS['price']

classTriples = [
	(productClass, rdfType, owlClass),
	(orderClass, rdfType, owlClass),
	(personClass, rdfType, owlClass),
	(paymentClass, rdfType, owlClass)
]

classHierarchyTriples = [
	# People
	(employeeClass, rdfsSubClassOf, personClass),
	(customerClass, rdfsSubClassOf, personClass),

	# Products
	(additionClass, rdfsSubClassOf, productClass),
	(coffeeClass, rdfsSubClassOf, productClass)
]

############
# PROPERTIES
############

propertyTriples = [

	# Products
	(price, rdfType, owlDatatypeProperty),
	(price, rdfsDomain, productClass),
	(price, rdfsRange, xsdDecimal),

	# Orders
	(orderId, rdfType, owlDatatypeProperty),
	(orderId, rdfsDomain, orderClass),
	(orderId, rdfsRange, xsdString),

	(orderStatus, rdfType, owlDatatypeProperty),
	(orderStatus, rdfsDomain, orderClass),
	(orderStatus, rdfsRange, xsdString),

	(orderTime, rdfType, owlDatatypeProperty),
	(orderTime, rdfsDomain, orderClass),
	(orderTime, rdfsRange, xsdDateTime),

	(paymentType, rdfType, owlDatatypeProperty),
	(paymentType, rdfsDomain, paymentClass),
	(paymentType, rdfsRange, xsdString),

	(orderedBy, rdfType, owlObjectProperty),
	(orderedBy, rdfsDomain, orderClass),
	(orderedBy, rdfsRange, customerClass),

	(orderIncludesProduct, rdfType, owlObjectProperty),
	(orderIncludesProduct, rdfsDomain, orderClass),
	(orderIncludesProduct, rdfsRange, productClass),

	# Person
	(fullName, rdfType, owlDatatypeProperty),
	(fullName, rdfsDomain, personClass),
	(fullName, rdfsRange, xsdString),

	# Employees
	(employeeRole, rdfType, owlDatatypeProperty),
	(employeeRole, rdfsDomain, employeeClass),
	(employeeRole, rdfsRange, xsdString),

	(employeeId, rdfType, owlDatatypeProperty),
	(employeeId, rdfsDomain, employeeClass),
	(employeeId, rdfsRange, xsdString),

	# Customers
	(customerId, rdfType, owlDatatypeProperty),
	(customerId, rdfsDomain, customerClass),
	(customerId, rdfsRange, xsdString),

	# Payments
	(paymentAssociatedWith, rdfType, owlObjectProperty),
	(paymentAssociatedWith, rdfsDomain, paymentClass),
	(paymentAssociatedWith, rdfsRange, orderClass)
]

from rdflib import ConjunctiveGraph
graph = ConjunctiveGraph()

for triple in classTriples:
	graph.add(triple)

for triple in classHierarchyTriples:
	graph.add(triple)

for triple in propertyTriples:
	graph.add(triple)


################
# INSTANCE DATA
################

# People
JimHay = coffeeNS['b3eae388-e8d2-4834-8284-a170aef489f3']
CliffObrecht = coffeeNS['c1ff0fff-7fd6-4698-a525-df7e6f426395']
MitchellBaker = coffeeNS['6ak3rbe5-aaf8-4c5d-a1a0-af9058eb9792']
TimBernersLee = coffeeNS['7im63rnr-8fd6-4698-o525-ff7e6f426391']
DanBrickley = coffeeNS['6r1ckl3y-8fd6-4698-o525-ff7e6f426391']
BartSimpson = coffeeNS['baeaa788-8fd6-4698-o525-ff7e6f426391']

# Coffees
espresso = coffeeNS['espresso']
latte = coffeeNS['latte']
flat_white = coffeeNS['flat_white']
cappuccino = coffeeNS['cappuccino']
piccolo = coffeeNS['piccolo']
iced_coffee = coffeeNS['iced_coffee']

# Additions 
soy = coffeeNS['soy']
almond = coffeeNS['almond']
skim = coffeeNS['skim']
large = coffeeNS['large']
decaf = coffeeNS['decaf']
extraShot = coffeeNS['extra-shot']

coffeeOntologyInstances = [

	# Coffee types
	(espresso, rdfType, coffeeClass),
	(espresso, price, Literal(3.0, datatype=xsdDecimal)),
	(latte, rdfType, coffeeClass),
	(latte, price, Literal(4.0, datatype=xsdDecimal)),
	(flat_white, rdfType, coffeeClass),
	(flat_white, price, Literal(4.0, datatype=xsdDecimal)),
	(cappuccino, rdfType, coffeeClass),
	(cappuccino, price, Literal(4.0, datatype=xsdDecimal)),
	(piccolo, rdfType, coffeeClass),
	(piccolo, price, Literal(4.0, datatype=xsdDecimal)),
	(iced_coffee, rdfType, coffeeClass),
	(iced_coffee, price, Literal(5.0, datatype=xsdDecimal)),

	# Additions
	(soy, rdfType, additionClass),
	(soy, price, Literal(0.5, datatype=xsdDecimal)),
	(almond, rdfType, additionClass),
	(almond, price, Literal(0.5, datatype=xsdDecimal)),
	(skim, rdfType, additionClass),
	(skim, price, Literal(0.5, datatype=xsdDecimal)),
	(large, rdfType, additionClass),
	(large, price, Literal(0.5, datatype=xsdDecimal)),
	(decaf, rdfType, additionClass),
	(decaf, price, Literal(0.5, datatype=xsdDecimal)),
	(extraShot, rdfType, additionClass),
	(extraShot, price, Literal(0.5, datatype=xsdDecimal)),

	# Customers
	(JimHay, rdfType, customerClass),
	(JimHay, fullName, Literal('Jim Hay', datatype=xsdString)),
	(JimHay, customerId, Literal('b3eae388-e8d2-4834-8284-a170aef489f3', datatype=xsdString)),

	(CliffObrecht, rdfType, customerClass),
	(CliffObrecht, fullName, Literal('Cliff Obrecht', datatype=xsdString)),
	(CliffObrecht, customerId, Literal('b3eae388-e8d2-4834-8284-a170aef489f3', datatype=xsdString)),

	(MitchellBaker, rdfType, customerClass),
	(MitchellBaker, fullName, Literal('Mitchell Baker', datatype=xsdString)),
	(MitchellBaker, customerId, Literal('6ak3rbe5-aaf8-4c5d-a1a0-af9058eb9792', datatype=xsdString)),

	# Employees
	(TimBernersLee, rdfType, employeeClass),
	(TimBernersLee, fullName, Literal('Tim Berners-Lee', datatype=xsdString)),
	(TimBernersLee, employeeRole, Literal('Barista', datatype=xsdString)),
	(TimBernersLee, employeeId, Literal('7im63rnr-8fd6-4698-o525-ff7e6f426391', datatype=xsdString)),

	(DanBrickley, rdfType, employeeClass),
	(DanBrickley, fullName, Literal('Dan Brickley', datatype=xsdString)),
	(DanBrickley, employeeRole, Literal('Cashier', datatype=xsdString)),
	(DanBrickley, employeeId, Literal('6r1ckl3y-8fd6-4698-o525-ff7e6f426391', datatype=xsdString)),

	(BartSimpson, rdfType, employeeClass),
	(BartSimpson, fullName, Literal('Bart Simpson', datatype=xsdString)),
	(BartSimpson, employeeRole, Literal('Manager', datatype=xsdString)),
	(BartSimpson, employeeId, Literal('baeaa788-8fd6-4698-o525-ff7e6f426391', datatype=xsdString)),

	# Orders
	(coffeeNS['3917ecf1-4be7-478f-8934-537cb1572c25'], rdfType, orderClass),
	(coffeeNS['3917ecf1-4be7-478f-8934-537cb1572c25'], orderId, Literal('3917ecf1-4be7-478f-8934-537cb1572c25', datatype=xsdString)),
	(coffeeNS['3917ecf1-4be7-478f-8934-537cb1572c25'], orderStatus, Literal('order-served', datatype=xsdString)),
	(coffeeNS['3917ecf1-4be7-478f-8934-537cb1572c25'], orderTime, Literal('2019-07-20T11:32:52', datatype=xsdDateTime)),
	(coffeeNS['3917ecf1-4be7-478f-8934-537cb1572c25'], orderedBy, JimHay),
	(coffeeNS['3917ecf1-4be7-478f-8934-537cb1572c25'], orderIncludesProduct, piccolo),
	(coffeeNS['3917ecf1-4be7-478f-8934-537cb1572c25'], orderIncludesProduct, almond),

	(coffeeNS['a0746122-d673-49dc-8f75-fa69c0f3ab7f'], rdfType, orderClass),
	(coffeeNS['a0746122-d673-49dc-8f75-fa69c0f3ab7f'], orderId, Literal('a0746122-d673-49dc-8f75-fa69c0f3ab7f', datatype=xsdString)),
	(coffeeNS['a0746122-d673-49dc-8f75-fa69c0f3ab7f'], orderStatus, Literal('order-served', datatype=xsdString)),
	(coffeeNS['a0746122-d673-49dc-8f75-fa69c0f3ab7f'], orderTime, Literal('2019-07-20T11:45:52', datatype=xsdDateTime)),
	(coffeeNS['a0746122-d673-49dc-8f75-fa69c0f3ab7f'], orderedBy, CliffObrecht),
	(coffeeNS['a0746122-d673-49dc-8f75-fa69c0f3ab7f'], orderIncludesProduct, latte),
	(coffeeNS['a0746122-d673-49dc-8f75-fa69c0f3ab7f'], orderIncludesProduct, extraShot),

	(coffeeNS['94e896e8-cb06-40cc-9765-0c351e00dbb3'], rdfType, orderClass),
	(coffeeNS['94e896e8-cb06-40cc-9765-0c351e00dbb3'], orderId, Literal('94e896e8-cb06-40cc-9765-0c351e00dbb3', datatype=xsdString)),
	(coffeeNS['94e896e8-cb06-40cc-9765-0c351e00dbb3'], orderStatus, Literal('order-served', datatype=xsdString)),
	(coffeeNS['94e896e8-cb06-40cc-9765-0c351e00dbb3'], orderTime, Literal('2019-07-20T11:45:52', datatype=xsdDateTime)),
	(coffeeNS['94e896e8-cb06-40cc-9765-0c351e00dbb3'], orderedBy, MitchellBaker),
	(coffeeNS['94e896e8-cb06-40cc-9765-0c351e00dbb3'], orderIncludesProduct, iced_coffee),

	(coffeeNS['8e77ae6f-7266-4d4f-881b-639ecf741ae3'], rdfType, orderClass),
	(coffeeNS['8e77ae6f-7266-4d4f-881b-639ecf741ae3'], orderId, Literal('8e77ae6f-7266-4d4f-881b-639ecf741ae3', datatype=xsdString)),
	(coffeeNS['8e77ae6f-7266-4d4f-881b-639ecf741ae3'], orderStatus, Literal('order-served', datatype=xsdString)),
	(coffeeNS['8e77ae6f-7266-4d4f-881b-639ecf741ae3'], orderTime, Literal('2019-07-21T11:32:52', datatype=xsdDateTime)),
	(coffeeNS['8e77ae6f-7266-4d4f-881b-639ecf741ae3'], orderedBy, JimHay),
	(coffeeNS['8e77ae6f-7266-4d4f-881b-639ecf741ae3'], orderIncludesProduct, piccolo),

	(coffeeNS['dc6cf8d8-d054-4616-9795-8f4ae47446df'], rdfType, orderClass),
	(coffeeNS['dc6cf8d8-d054-4616-9795-8f4ae47446df'], orderId, Literal('94e896e8-cb06-40cc-9765-0c351e00dbb3', datatype=xsdString)),
	(coffeeNS['dc6cf8d8-d054-4616-9795-8f4ae47446df'], orderStatus, Literal('order-placed', datatype=xsdString)),
	(coffeeNS['dc6cf8d8-d054-4616-9795-8f4ae47446df'], orderTime, Literal('2019-07-22T11:32:52', datatype=xsdDateTime)),
	(coffeeNS['dc6cf8d8-d054-4616-9795-8f4ae47446df'], orderedBy, JimHay),
	(coffeeNS['dc6cf8d8-d054-4616-9795-8f4ae47446df'], orderIncludesProduct, cappuccino),
	(coffeeNS['dc6cf8d8-d054-4616-9795-8f4ae47446df'], orderIncludesProduct, large)
]

for triple in coffeeOntologyInstances: graph.add(triple) 


################
# SPARQL QUERIES
################


# 1.List all coffee orders received before noon on 20-07-2019 

qres = graph.query(
    		"""PREFIX ex:<http://www.z3207120.unsw.edu.au/ontology#>
			SELECT DISTINCT ?order ?orderTime
			WHERE { ?order a ex:Order;
				           ex:orderTime ?orderTime ;
		 	FILTER (?orderTime < "2019-07-20T12:00:00"^^xsd:dateTime)}"""
		 	)

print("Q1")
for row in qres:
    print("OrderID: %s , orderTime: %s" % row)


# 2. List all the customers who ordered coffee on 20-07-2019
qres = graph.query(
    		"""PREFIX ex:<http://www.z3207120.unsw.edu.au/ontology#>
			SELECT DISTINCT ?order ?orderTime ?customer
			WHERE { ?order a ex:Order;
						   ex:orderedBy ?customer ;
				           ex:orderTime ?orderTime ;
		 	FILTER (?orderTime > "2019-07-20T00:00:00"^^xsd:dateTime  
					&&
			?orderTime < "2019-07-21T00:00:00"^^xsd:dateTime)}"""
			)
print("Q2")
for row in qres:
    print("orderID: %s , orderTime: %s , customerID: %s" % row)



# 3.List available coffee types and their prices
qres = graph.query(
    """PREFIX ex:<http://www.z3207120.unsw.edu.au/ontology#>
	   SELECT DISTINCT ?product ?price
	   WHERE { ?product ex:price ?price ;
		 				a ex:Coffee .}"""
		 		)
print("Q3")
for row in qres:
    print("Product: %s , price: %s" % row) 


# 4.List all the employees of the coffee shop with their role. 
qres = graph.query(
    """PREFIX ex:<http://www.z3207120.unsw.edu.au/ontology#>
	   SELECT ?employee ?role ?name
	   WHERE { ?employee ex:employeeRole ?role .
			   ?employee ex:fullName ?name . }"""
			      )
print("Q4")
for row in qres:
    print("Employee ID: %s , role: %s , name %s" % row)


################
# OUTPUT GRAPH
################

graph.serialize(destination='z3207120_coffeeshop.ttl', format='turtle')












