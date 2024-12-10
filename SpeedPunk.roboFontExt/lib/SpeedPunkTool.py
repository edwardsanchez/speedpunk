##########################################################################################
#
#	Speed Punk
#	Visualisation tool of outline curvature for font editors.
#	
#	Distributed under Apache 2.0 license
#
##########################################################################################

import traceback
from AppKit import NSLog

try:

	from mojo.events import installTool, EditingTool
	from deYanoneRoboFontSpeedpunk import speedpunklib
	from mojo.extensions import ExtensionBundle
	bundle = ExtensionBundle("SpeedPunk")


	################################################################################################################

	class SpeedPunkTool(EditingTool):

		def becomeActive(self):
			self.speedpunklib = speedpunklib.SpeedPunkLib()
			self.speedpunklib.tool = self
			self.speedpunklib.Open()

		def becomeInactive(self):
			self.speedpunklib.Close()

		def drawBackground(self, scale):
			if not self.getGlyph():
				return
			
			glyph = self.getGlyph()
			
			# Get selected points
			selected_points = []
			for contour in glyph:
				for point in contour.points:
					if point.selected and point.type in ['curve', 'line']:  # Only get on-curve points
						selected_points.append(point)
			
			# Only proceed if we have 2 or more points selected
			if len(selected_points) >= 2:
				# Clear existing visualization
				self.speedpunklib.curvesegments = []
				
				# Find segments between selected points
				for contour in glyph:
					for i, point in enumerate(contour.points):
						if point.type == 'curve' and point.selected:
							# Get the previous on-curve point
							prev_point = None
							for p in reversed(contour.points[:i]):
								if p.type in ['curve', 'line']:
									prev_point = p
									break
							
							# If previous point is also selected, show this segment
							if prev_point and prev_point.selected:
								self.speedpunklib.UpdateGlyph(glyph, selected_segment=(prev_point, point))
			else:
				# Clear any existing visualization
				self.speedpunklib.curvesegments = []

		def glyphWindowWillClose(self, a):
			self.speedpunklib.Close()

		def glyphWindowDidOpen(self, a):
			self.speedpunklib.Open()

		def getToolbarTip(self):
			return "Speed Punk"

		def getToolbarIcon(self):
			NSImage = bundle.getResourceImage("toolbar")
			if NSImage:
				return NSImage

	installTool(SpeedPunkTool())

except:
	NSLog('Speed Punk:\n%s' % traceback.format_exc())