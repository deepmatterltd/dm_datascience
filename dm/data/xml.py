# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 12:42:21 2019

@author: Deepmatter
"""

from lxml import etree
from signxml import XMLVerifier

def validate_xml(xml_file, schema_file):
    """Validate that an XML document adheres to a XSD schema.    

    Parameters
    ----------
    xml_file : String
        Path to an XML file.
    schema_file : String
        Path to an XSD file.

    Returns
    -------
    None.
    
    Raises
    ------
    DocumentInvalid 
        If the document is not compliant with the schema.

    """
    
    xml_doc = etree.parse(xml_file)
    xml_schema = etree.XMLSchema(etree.parse(schema_file))
    
    xml_schema.assertValid(xml_doc)

        
def verify_x509_signature(xml_file, cer_file):
    """Verifies (asserts) that a signed XML file was generated using a certificate.    

    Parameters
    ----------
    xml_file : String
        Path to an XML file.
    cer_file : String
        Path to an X.509 certificate.

    Returns
    -------
    None.
    
    Raises
    ------
    signxml.InvalidSignature
        If the signature is not valid.

    """

    cert = open(cer_file, "rb").read()
    xml_elem = etree.parse(xml_file)

    XMLVerifier().verify(xml_elem, x509_cert = cert)
    
def transform(xml_file, xslt_file, outfile = None):
    """Transform an XML document by an XSL transform.

    Parameters
    ----------
    xml_file : String
        Path to an XML file.
    xslt_file : String
        Path to an XSLT file.
    outfile : String, optional
        Path to an output HTML file. The default is None.

    Returns
    -------
    Integer or String
        By default returns the HTML generatd by the transformation. If
        "outfile" is non-null, returns the number of characters written to disk.

    """
    
    xml_obj = etree.parse(xml_file)
    xslt_obj = etree.parse(xslt_file)
    
    transform = etree.XSLT(xslt_obj)
    xml_obj_transform = transform(xml_obj)
    html_xml = etree.tostring(xml_obj_transform, pretty_print=False)
    
    if outfile is not None:
        with open(outfile, 'w') as outstream:
            return outstream.write(html_xml.decode("utf8"))
    else:
        return html_xml
    