#!/usr/bin/env python
# coding: utf-8

# # Your Chemistry, Your Data, Your Insights
# #### 02/12/2019
# 

# Specify some constants referring to the input XML files and schemas. We'll work with these for the rest of this notebook.

# # Validating PCML and PCRR
# 
# Use the lxml library to validate that our recipe PCML and runtime PCRR adheres to the respective standards.

# In[ ]:


from lxml import etree

pcml_schema_file = './data/pcml-1.3.4.xsd'
pcml_recipe_file = './data/3a_recipe.pcml'

pcrr_schema_file = './data/pcrr-0.0.1.xsd'
pcrr_recipe_files = ['./data/3a_run_01.pcrr',
                     './data/3a_run_02.pcrr',
                     './data/3a_run_03.pcrr']


# In[ ]:


def validate_xml(xml_file, schema_file):
    try:
        xml_doc = etree.parse(xml_file)
        xml_schema = etree.XMLSchema(etree.parse(schema_file))
        
        xml_schema.assertValid(xml_doc)

        print("XML for '{}' is valid".format(xml_file))
    except etree.DocumentInvalid as e:
        print("ERROR: XML for '{} is invalid".format(xml_file))
        raise
    except:
        print("There was an error while validating the XML")
        raise


# In[ ]:


#validate the PCML against its XSD schema

validate_xml(pcml_recipe_file, pcml_schema_file)


# In[ ]:


#verify the signatures in all PCRR files.
for rr in pcrr_recipe_files:
    validate_xml(rr, pcrr_schema_file)
    


# # Verifying X.509 Signatures

# Now let's validate the X509 certificate. As this is self signed, it is included in the same directory as the data.

# In[ ]:


from signxml import XMLVerifier, InvalidSignature

def verify_x509_signature(xml_file, cer_file):
    
    try:
        cert = open(cer_file, "rb").read()
        xml_elem = etree.parse(xml_file)

        verified_data = XMLVerifier().verify(xml_elem, x509_cert = cert)
        print("X.509 signature of '{}' is valid as generated by DigitalGlassware".format(xml_file))

        return
    except InvalidSignature:
        print("X.509 signature for '{}' is invalid -- it may not have been generated by DigitalGlassware, or has been modified after signing.".format(xml_file))
        raise
    except:
        print("An error occurred whilst verifying X.509 signature of '{}'".format(xml_file))
        raise


# In[ ]:


#verify the X509 signature of the PCML
pcml_cer_path = "./data/x509/pcml.crt"
verify_x509_signature(pcml_recipe_file, pcml_cer_path)


# In[ ]:


#verify the signatures in all PCRR files.

pcrr_cer_path = "./data/x509/pcrr.crt"

for rr in pcrr_recipe_files:
    verify_x509_signature(rr, pcrr_cer_path)


# # Transforming PCML

# In[ ]:


#apply an XSL transformation to the PCML data

pcml_xslt_flow_file = "./data/flow.xsl"

pcml_obj = etree.parse(pcml_recipe_file)
xslt_obj = etree.parse(pcml_xslt_flow_file)

transform = etree.XSLT(xslt_obj)
pcml_obj_transform = transform(pcml_obj)
html_xml = etree.tostring(pcml_obj_transform, pretty_print=False)

with open("./out/3a_pcml_flow.html", 'w') as outfile:
    outfile.write(html_xml.decode("utf8"))


# # Extracting Recipe Content

# In[ ]:


#list all the chemicals used
chem_elem = pcml_obj.find(".//chemicals")
for c in chem_elem:
    print("Chemical: {}".format(c[0].text))
    


# In[ ]:


#search for specific safety code
import itertools

code_to_search = "H318"
has_code = len(pcml_obj.xpath('.//safetycode/code[text()="{}"]'.format(code_to_search))) > 0
print("{} {} code associated with recipe chemicals".format("Found" if has_code else "Did not find", code_to_search))


# In[ ]:


#List off safety codes
safety_elem = pcml_obj.findall(".//safetycode/code")
all_s_codes = [s.text for s in safety_elem]

uniq_s_codes = set(itertools.chain.from_iterable([x.split(" + ") for x in all_s_codes]))
print("Found the following unique safety codes:", sorted(uniq_s_codes))


# In[ ]:


#extract and count roles of chemicals
from collections import Counter
import pprint

role_elems = pcml_obj.xpath('.//chemicals/chemical')
role_counts = Counter([r.get("role", None) for r in role_elems])

pp = pprint.PrettyPrinter()
pp.pprint(role_counts)


# In[ ]:


#get durations of recipes
from datetime import datetime

time_fmt = "%Y-%m-%dT%H:%M:%S.%f%z"

for i, rr in enumerate(pcrr_recipe_files, 1):
    
    start_str = next(etree.iterparse(rr, tag = "start_time"))[1].text
    end_str = next(etree.iterparse(rr, tag = "end_time"))[1].text
    
    start_datetime = datetime.strptime(start_str, time_fmt)
    end_datetime = datetime.strptime(end_str, time_fmt)
    
    rr_duration = end_datetime - start_datetime
    print("Duration of recipe run {} is {}".format(i, rr_duration))
    

