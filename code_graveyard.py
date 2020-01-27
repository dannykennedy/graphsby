# # Get all items
# q = graph.query(
#     """PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
# 	   SELECT DISTINCT ?item ?description ?layout ?handle
# 	   WHERE {
# 	   			?item dnj:layout ?layout .
# 	   			?item dnj:handle ?handle .
# 	   			?item dnj:description ?description .
# 	   			?item rdf:type/rdfs:subClassOf* dnj:Item .}"""
# 		 		)

# print("Items: ")
# # for row in q:
# #     print("Item: %s , Description %s , Layout %s, Handle: %s" % row)
# #     # print(row) 

# print(len(q))

# # Get all items
# q = graph.query(
#     """PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
# 	   SELECT DISTINCT ?item
# 	   WHERE { ?network dnj:handle "dreamnetwork"^^xsd:string .
# 	   		   ?item dnj:hasTag ?network .
# 	   			}"""
# 		 		)

# print("Items: ")
# # for row in q:
# 	# print("Itemzzzz: %s" % row)
#     # print(row) 

# print(len(q))