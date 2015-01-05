#!/usr/bin/env python

import sys
from os import sep
import ConfigParser
import fnmatch

from Debug import *  # dprint()



options = { \
    'playlistsview'             :('List', 'Hide'), \
    'libraryview'       :('List', 'Grid', 'Bookcase', 'Hide'), \
    'libraryview_remote'       :('List', 'Grid', 'Bookcase', 'Hide'), \
    'movieview'         :('Grid', 'List', 'Detailed List', 'Artwork'), \
    'homevideoview'     :('List', 'Grid', 'Detailed List'), \
    'actorview'         :('Movies', 'Portrait'), \
    'showview'          :('Detailed List', 'List', 'Grid', 'Artwork'), \
    'flattenseason'     :('False', 'True'), \
    'seasonview'        :('List', 'Artwork', 'Coverflow'), \
    'channelview'       :('List', 'Grid', 'Bookcase', 'Hide'), \
    'durationformat'    :('Hours/Minutes', 'Minutes'), \
    'moviefanart'       :('Hide', 'Show'), \
    'tvshowfanart'          :('Hide', 'Show'), \
    'fanart'          :('Fanart', 'Banner'), \
    'fanart_blur'           :('0', '5', '10', '15', '20'), \
    'moviepreplay_bottomshelf'  :('Others Starring', 'Extras', 'Related Movies'), \
    'showtitles_movies'         :('Show All', 'Highlighted Only'), \
    'showtitles_tvshows'        :('Show All', 'Highlighted Only'), \
    'showtitles_homevideos'     :('Show All', 'Highlighted Only'), \
    'showtitles_channels'       :('Show All', 'Highlighted Only'), \
    'movies_navbar_ondeck'      :('unchecked', 'checked'), \
    'movies_navbar_unwatched'   :('unchecked', 'checked'), \
    'movies_navbar_byfolder'    :('unchecked', 'checked'), \
    'movies_navbar_collections' :('unchecked', 'checked'), \
    'movies_navbar_genres'      :('unchecked', 'checked'), \
    'movies_navbar_decades'     :('unchecked', 'checked'), \
    'movies_navbar_directors'   :('unchecked', 'checked'), \
    'movies_navbar_actors'      :('unchecked', 'checked'), \
    'movies_navbar_more'        :('unchecked', 'checked'), \
    'homevideos_navbar_ondeck'      :('unchecked', 'checked'), \
    'homevideos_navbar_unwatched'   :('unchecked', 'checked'), \
    'homevideos_navbar_byfolder'    :('unchecked', 'checked'), \
    'homevideos_navbar_collections' :('unchecked', 'checked'), \
    'homevideos_navbar_genres'      :('unchecked', 'checked'), \
    'music_navbar_recentlyadded'    :('unchecked', 'checked'), \
    'music_navbar_genre'            :('unchecked', 'checked'), \
    'music_navbar_decade'           :('unchecked', 'checked'), \
    'music_navbar_year'             :('unchecked', 'checked'), \
    'music_navbar_more'             :('unchecked', 'checked'), \
    'tv_navbar_ondeck'          :('unchecked', 'checked'), \
    'tv_navbar_unwatched'       :('unchecked', 'checked'), \
    'tv_navbar_genres'          :('unchecked', 'checked'), \
    'tv_navbar_more'            :('unchecked', 'checked'), \
    'transcodequality'  :('1080p 40.0Mbps', \
                          '480p 2.0Mbps', \
                          '720p 3.0Mbps', '720p 4.0Mbps', \
                          '1080p 8.0Mbps', '1080p 10.0Mbps', '1080p 12.0Mbps', '1080p 20.0Mbps'), \
    'transcoderaction'  :('Auto', 'DirectPlay', 'Transcode'), \
    'remotebitrate'     :('720p 3.0Mbps', '720p 4.0Mbps', \
                          '1080p 8.0Mbps', '1080p 10.0Mbps', '1080p 12.0Mbps', '1080p 20.0Mbps', '1080p 40.0Mbps', \
                          '480p 2.0Mbps'), \
    'phototranscoderaction'     :('Auto', 'Transcode'), \
    'subtitlerenderer'  :('Auto', 'iOS, PMS', 'PMS'), \
    'subtitlesize'      :('100', '125', '150', '50', '75'), \
    'audioboost'        :('100', '175', '225', '300'), \
    'showunwatched'     :('True', 'False'), \
    'showsynopsis'      :('Show', 'Hide'), \
    'showplayerclock'   :('True', 'False'), \
    'showplayinfos'             :('True', 'False'), \
    'overscanadjust'    :('0', '1', '2', '3', '-3', '-2', '-1'), \
    'clockposition'     :('Right', 'Center', 'Left'), \
    'showendtime'       :('True', 'False'), \
    'timeformat'        :('24 Hour', '12 Hour'), \
    'myplex_user'       :('', ), \
    'myplex_auth'       :('', ), \
    }



class CATVSettings():
    def __init__(self):
        dprint(__name__, 1, "init class CATVSettings")
        self.cfg = None
        self.loadSettings()
    
    
    
    # load/save config
    def loadSettings(self):
        dprint(__name__, 1, "load settings")
        # options -> default
        dflt = {}
        for opt in options:
            dflt[opt] = options[opt][0]
        
        # load settings
        self.cfg = ConfigParser.SafeConfigParser(dflt)
        self.cfg.read(self.getSettingsFile())
    
    def saveSettings(self):
        dprint(__name__, 1, "save settings")
        f = open(self.getSettingsFile(), 'wb')
        self.cfg.write(f)
        f.close()
    
    def getSettingsFile(self):
        return sys.path[0] + sep + "ATVSettings.cfg"
    
    def checkSection(self, UDID):
        # check for existing UDID section
        sections = self.cfg.sections()
        if not UDID in sections:
            self.cfg.add_section(UDID)
            dprint(__name__, 0, "add section {0}", UDID)
    
    
    
    # access/modify AppleTV options
    def getSetting(self, UDID, option):
        self.checkSection(UDID)
        dprint(__name__, 1, "getsetting {0}", self.cfg.get(UDID, option))
        return self.cfg.get(UDID, option)
    
    def setSetting(self, UDID, option, val):
        self.checkSection(UDID)
        self.cfg.set(UDID, option, val)
    
    def checkSetting(self, UDID, option):
        self.checkSection(UDID)
        val = self.cfg.get(UDID, option)
        opts = options[option]
        
        # check val in list
        found = False
        for opt in opts:
            if fnmatch.fnmatch(val, opt):
                found = True
        
        # if not found, correct to default
        if not found:
            self.cfg.set(UDID, option, opts[0])
            dprint(__name__, 1, "checksetting: default {0} to {1}", option, opts[0])
    
    def toggleSetting(self, UDID, option):
        self.checkSection(UDID)
        cur = self.cfg.get(UDID, option)
        opts = options[option]
    
        # find current in list
        i=0
        for i,opt in enumerate(opts):
            if opt==cur:
                break
    
        # get next option (circle to first)
        i=i+1
        if i>=len(opts):
            i=0
    
        # set
        self.cfg.set(UDID, option, opts[i])
    
    def setOptions(self, option, opts):
        global options
        if option in options:
            options[option] = opts
            dprint(__name__, 1, 'setOption: update {0} to {1}', option, opts)



if __name__=="__main__":
    ATVSettings = CATVSettings()
    
    UDID = '007'
    ATVSettings.checkSection(UDID)
    
    option = 'transcodequality'
    print ATVSettings.getSetting(UDID, option)
    
    print "setSetting"
    ATVSettings.setSetting(UDID, option, 'True')  # error - pick default
    print ATVSettings.getSetting(UDID, option)
    ATVSettings.setSetting(UDID, option, '9')
    print ATVSettings.getSetting(UDID, option)
    
    print "toggleSetting"
    ATVSettings.toggleSetting(UDID, option)
    print ATVSettings.getSetting(UDID, option)
    ATVSettings.toggleSetting(UDID, option)
    print ATVSettings.getSetting(UDID, option)
    ATVSettings.toggleSetting(UDID, option)
    print ATVSettings.getSetting(UDID, option)
    
    del ATVSettings
