# encoding: utf-8
from __future__ import division, print_function, unicode_literals

##########################################################################################
#
#	Speed Punk
#	Visualisation tool of outline curvature for font editors.
#	
#	Distributed under Apache 2.0 license
#
##########################################################################################

import objc, webbrowser
from GlyphsApp import *
from GlyphsApp import NSStr
from GlyphsApp.plugins import *
from Foundation import NSString
from AppKit import NSGraphicsContext, NSUserDefaultsController, NSLog

import speedpunk.speedpunklib

# import cProfile, pstats
# def gprofile(self, layer, command):
	
# 	filename = 'profile_stats.stats'
# 	#profile.run(command, filename)
# 	cProfile.runctx(command, globals(), locals(), filename)

# 	# Read all 5 stats files into a single object
# 	stats = pstats.Stats(filename)
# 	# Clean up filenames for the report
# 	stats.strip_dirs()
# 	# Sort the statistics by the cumulative time spent in the function
# 	stats.sort_stats('cumulative')
# 	stats.print_stats()

class GlyphsAppSpeedPunkReporter(ReporterPlugin):
	
	settingsView = objc.IBOutlet()
	gainSlider = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		NSLog("SpeedPunk plugin is loading!")  # Add this line - should print when Glyphs starts
		self.keyboardShortcut = 'x'
		self.menuName = 'Speed Punk TEST'  # Changed from 'Speed Punk' to 'Speed Punk TEST'
		
		curveGain = speedpunk.speedpunklib.curveGain
		self.loadNib('settingsView', __file__)
		self.speedpunklib = speedpunk.speedpunklib.SpeedPunkLib()
		self.speedpunklib.tool = self
		self.generalContextMenus = [{'name': 'Speed Punk', 'view': self.settingsView}]
		self.gainSlider.setMinValue_(curveGain[0])
		self.gainSlider.setMaxValue_(curveGain[1])
		
		self.histWidth = 200
		self.histHeight = 20
		
		default = NSUserDefaultsController.sharedUserDefaultsController()
		default.addObserver_forKeyPath_options_context_(self, NSStr('values.de.yanone.speedPunk.illustrationPositionIndex'), 0, None)
		default.addObserver_forKeyPath_options_context_(self, NSStr('values.de.yanone.speedPunk.curveGain'), 0, None)
		default.addObserver_forKeyPath_options_context_(self, NSStr('values.de.yanone.speedPunk.useFader'), 0, None)
		default.addObserver_forKeyPath_options_context_(self, NSStr('values.de.yanone.speedPunk.fader'), 0, None)
	
	@objc.python_method
	def conditionsAreMetForDrawing(self):
			"""
			Don't activate if text or pan (hand) tool are active.
			"""
			currentController = self.controller.view().window().windowController()
			if currentController:
				tool = currentController.toolDrawDelegate()
				textToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolText") )
				handToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolHand") )
				if not textToolIsActive and not handToolIsActive: 
					return True
			return False
	
	def observeValueForKeyPath_ofObject_change_context_(self, keypath, observed, changed, context):
		self.speedpunklib.loadPreferences()
		Glyphs.redraw()
	
	@objc.python_method
	def background(self, layer):
		    NSColor.redColor().set()
    NSBezierPath.fillRect_(((0, 0), (50, 50)))

		# Try multiple logging approaches
		print("SPEEDPUNK DEBUG: Running new version")
		NSLog("SPEEDPUNK DEBUG: Running new version via NSLog")
		import sys
		sys.stderr.write("SPEEDPUNK DEBUG: Running new version via stderr\n")
		
		if self.conditionsAreMetForDrawing():
			selected_nodes = []
			for path in layer.paths:
				for node in path.nodes:
					if node.selected:
						selected_nodes.append(node)
			
			print("SPEEDPUNK DEBUG: Found %d selected nodes" % len(selected_nodes))
			
			# Only proceed if we have 2 or more nodes selected
			if len(selected_nodes) >= 2:
				# Create a temporary layer with only the segments between selected nodes
				temp_layer = GSLayer()
				for path in layer.paths:
					for i, node in enumerate(path.nodes):
						if node.type == CURVE and node.selected:
							# Check if previous node is also selected
							prev_node = path.nodes[i-3]  # Get the previous on-curve point
							if prev_node.selected:
								# Include this segment in visualization
								self.speedpunklib.UpdateGlyph(layer, selected_segment=(prev_node, node))
			else:
				# Clear any existing visualization
				self.speedpunklib.curvesegments = []
				self.speedpunklib.UpdateGlyph(layer)
	
	def drawForegroundWithOptions_(self, options):
		if self.speedpunklib.useFader:
			visibleRect = self.controller.viewPort
			histOriginX = NSMinX(visibleRect) + 10
			histOriginY = NSMaxY(visibleRect) - 10 - self.histHeight
			NSGraphicsContext.currentContext().saveGraphicsState()
			clippingPath = NSBezierPath.bezierPathWithRoundedRect_cornerRadius_(NSRect((histOriginX, histOriginY), (self.histWidth, self.histHeight)), 5)
			clippingPath.addClip()
			self.speedpunklib.drawGradient(histOriginX, histOriginY, self.histWidth, self.histHeight)
			self.speedpunklib.drawHistogram(histOriginX, histOriginY, self.histWidth, self.histHeight)
			NSGraphicsContext.currentContext().restoreGraphicsState()
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

	@objc.IBAction
	def visitWebsite_(self, sender):
		webbrowser.open_new_tab('https://github.com/yanone/speedpunk')

	@objc.IBAction
	def visitTwitter_(self, sender):
		webbrowser.open_new_tab('https://twitter.com/yanone')
