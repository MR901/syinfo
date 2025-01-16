
# ============================================================================ #
# Commands
# ---------------------------------------------------------------------------- #

# Get API Token if not already present
# login https://pypi.org/manage/projects/
# goto https://pypi.org/manage/account/token/
# create new token for syinfo project
# follow steps below


(syinfo) $ pip3 install twine
(syinfo) $ python3 setup.py sdist

        running sdist
        running egg_info
        creating syinfo.egg-info
        writing syinfo.egg-info/PKG-INFO
        writing dependency_links to syinfo.egg-info/dependency_links.txt
        writing entry points to syinfo.egg-info/entry_points.txt
        writing requirements to syinfo.egg-info/requires.txt
        writing top-level names to syinfo.egg-info/top_level.txt
        writing manifest file 'syinfo.egg-info/SOURCES.txt'
        file syinfo.py (for module syinfo) not found
        reading manifest file 'syinfo.egg-info/SOURCES.txt'
        adding license file 'LICENSE'
        writing manifest file 'syinfo.egg-info/SOURCES.txt'
        running check
        creating syinfo-0.0.2
        creating syinfo-0.0.2/syinfo
        creating syinfo-0.0.2/syinfo.egg-info
        copying files to syinfo-0.0.2...
        copying LICENSE -> syinfo-0.0.2
        copying README.rst -> syinfo-0.0.2
        copying setup.py -> syinfo-0.0.2
        copying syinfo/__init__.py -> syinfo-0.0.2/syinfo
        copying syinfo/__main__.py -> syinfo-0.0.2/syinfo
        copying syinfo/_version.py -> syinfo-0.0.2/syinfo
        copying syinfo/constants.py -> syinfo-0.0.2/syinfo
        copying syinfo/device_info.py -> syinfo-0.0.2/syinfo
        copying syinfo/network_info.py -> syinfo-0.0.2/syinfo
        copying syinfo/search_network.py -> syinfo-0.0.2/syinfo
        copying syinfo/sys_info.py -> syinfo-0.0.2/syinfo
        copying syinfo/utils.py -> syinfo-0.0.2/syinfo
        copying syinfo.egg-info/PKG-INFO -> syinfo-0.0.2/syinfo.egg-info
        copying syinfo.egg-info/SOURCES.txt -> syinfo-0.0.2/syinfo.egg-info
        copying syinfo.egg-info/dependency_links.txt -> syinfo-0.0.2/syinfo.egg-info
        copying syinfo.egg-info/entry_points.txt -> syinfo-0.0.2/syinfo.egg-info
        copying syinfo.egg-info/not-zip-safe -> syinfo-0.0.2/syinfo.egg-info
        copying syinfo.egg-info/requires.txt -> syinfo-0.0.2/syinfo.egg-info
        copying syinfo.egg-info/top_level.txt -> syinfo-0.0.2/syinfo.egg-info
        copying syinfo.egg-info/SOURCES.txt -> syinfo-0.0.2/syinfo.egg-info
        Writing syinfo-0.0.2/setup.cfg
        creating dist
        Creating tar archive
        removing 'syinfo-0.0.2' (and everything under it)

(syinfo) $ twine upload dist/syinfo-0.0.2.tar.gz --verbose

<<< API token

        Uploading distributions to https://upload.pypi.org/legacy/
        INFO     dist/syinfo-0.0.2.tar.gz (35.9 KB)                                                                      
        INFO     username set by command options                                                                         
        INFO     Querying keyring for password                                                                           
        Enter your API token: 
        INFO     username: __token__                                                                                     
        INFO     password: <hidden>                                                                                      
        Uploading syinfo-0.0.2.tar.gz
        100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 88.6/88.6 kB • 00:00 • 166.8 MB/s
        INFO     Response from https://upload.pypi.org/legacy/:                                                          
                 200 OK                                                                                                  
        INFO     <html>                                                                                                  
                  <head>                                                                                                 
                   <title>200 OK</title>                                                                                 
                  </head>                                                                                                
                  <body>                                                                                                 
                   <h1>200 OK</h1>                                                                                       
                   <br/><br/>                                                                                            
                                                                                                                         
                                                                                                                         
                                                                                                                         
                  </body>                                                                                                
                 </html>                                                                                                 

        View at:
        https://pypi.org/project/syinfo/0.0.2/

(syinfo) $ sudo ./cleanup.sh

# ============================================================================ #
