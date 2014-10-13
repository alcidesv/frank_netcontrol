from __future__ import print_function, absolute_import

from flask import json, request, make_response
import re
import os.path 
import os 
import glob
import gzip
import sys
import subprocess

from .app import app

DOCS_PATH= os.path.normpath( 
    os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), 'docs' ) )

@app.route("/rest/documentation_nodes")
def documentation_nodes(  ):
    results = []
    for filename in glob.glob(os.path.join(DOCS_PATH, "*.md" ) ):
        basename = os.path.basename( filename )
        results.append( {
            'md_name': basename, 
            'id':basename,
            'documentation_text_id': basename,
        })
    return json.jsonify(
        documentation_nodes = results
        )

@app.route("/rest/documentation_nodes/<which_one>")
def documentation_nodes2( which_one  ):
    filename = os.path.join( DOCS_PATH, which_one )
    if not os.path.exists( filename ):
        return "---not-found---", 404
    with open( filename, 'r') as fin:
        contents = fin.read()
    basename = os.path.basename(filename)
    return json.jsonify(
        documentation_node = {
            'id': basename,
            'md_name': basename,
            'documentation_text_id': basename
        })        
    
@app.route("/rest/documentation_texts/<which_one>")
def documentation_text( which_one ):    
    # Look for that node, if it exists
    filename = os.path.join( DOCS_PATH, which_one )
    if not os.path.exists( filename ):
        return "---not-found---", 404
    with open( filename, 'r') as fin:
        contents = fin.read()
    basename = os.path.basename(filename)
    return json.jsonify(
        documentation_text = {
            'id': basename,
            'md_text': contents,
            'documentation_node_id': basename
        })    

number_schme_re = re.compile(r"\.(\d)$")
@app.route("/rest/man_pages/<which_one>")
def man_page( which_one ):
    mo = number_schme_re.search( which_one )
    if mo == None:
        return ("Man page not found", 404 )
    
    subject = which_one[:(mo.start(1)-1)]
    d = mo.group(1)
    find_in_dir = os.path.join("/usr/share/man", "man" + d )
    gz_file = os.path.join( find_in_dir, which_one + ".gz" )
    
    p = subprocess.Popen([
        "man",
        str(d),
        subject
        ],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
        )
    
    (man_as_text, stderr ) = p.communicate()
    if p.wait() != 0 or stderr not in ("",None) :
        print( "Man: ", stderr, file=sys.stderr )
        return "Error rendering manpage", 500
    p = subprocess.Popen(
        ["man2html",
         "--bare",
         "-cgiurl",
         "\#/documentation-nodes/viewman/$title.$section"
         ],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
        )        
    (htmlized, stderr) = p.communicate( man_as_text )
    return json.jsonify( man_page = {
            'htmlized': htmlized,
            'title': subject,
            'section': int(d),
            'id': which_one
        })
    
