# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 17:13:09 2021

@author: ilros
"""
"""
REST server main file
"""


import cherrypy
from REST_classes.system_classes import GET_manager, POST_manager
from pyngrok import ngrok


class HouseRecoveryCatalog(object):
    
    def __init__(self):
        pass
    
    exposed=True
    @cherrypy.tools.json_out()  
    @cherrypy.tools.json_in()
    
    def POST(self, *path):
        data=cherrypy.request.json
        objPOST=POST_manager(path)
        objPOST.run(data)
        
        
    def GET(self, *path):
        objGET=GET_manager(path)
        output_get=objGET.run()
        return output_get

    
    def PUT(self):
        pass
    
    def DELETE(self):
        pass
    

if __name__=='__main__':
    conf={
        '/': {
            'request.dispatch':cherrypy.dispatch.MethodDispatcher()
            }
        }
    
    
    objServer=HouseRecoveryCatalog()
    cherrypy.tree.mount(objServer, '/', conf)
    

    
    cherrypy.engine.start()

    cherrypy.engine.block()