//
//  SpeedPunk.h
//  SpeedPunk
//
//  Created by Georg Seifert on 27.09.23.
//
//

#import <Cocoa/Cocoa.h>
#import <GlyphsCore/GlyphsReporterProtocol.h>
#import <GlyphsCore/GSPathSegment.h>

@interface SPSpeedPunk : NSViewController <GlyphsReporter>

@property (weak) IBOutlet NSSlider *gainSlider;
@property (weak) IBOutlet NSTextField *titleField;

//@property (nonatomic, strong) NSMutableArray<GSPathSegment *> *segments; //Unknown type name 'GSPathSegment'

@end
