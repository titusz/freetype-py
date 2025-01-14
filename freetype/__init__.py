#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
FreeType high-level python API 

This the bindings for the high-level API of FreeType (that must be installed
somewhere on your system).

Note:
-----
C Library will be searched using the ctypes.util.find_library. However, this
search might fail. In such a case (or for other reasons), you can specify the
FT_library_filename before importing the freetype library and freetype will use
the specified one. 
'''
from ctypes import *
from ft_types import *
from ft_enums import *
from ft_errors import *
from ft_structs import *
import ctypes.util
import os

PACKAGE_FOLDER = os.path.abspath(os.path.dirname(__file__))


__dll__    = None
__handle__ = None
FT_Library_filename = ctypes.util.find_library('freetype')

if not FT_Library_filename:
    
    paths_to_try = [ os.path.join(PACKAGE_FOLDER, 'libfreetype.dll'), # Windows
                     'libfreetype.so.6',  # Linux
                     '/usr/X11/lib/libfreetype.dylib', # MacOS X
                   ]
    for p in paths_to_try:
        try:
            __dll__ = CDLL(p)
        except OSError:
            pass
            
        if __dll__ is not None:
            break
if not FT_Library_filename and not __dll__:
    raise RuntimeError, 'Freetype library not found'
if not __dll__:
    __dll__ = CDLL(FT_Library_filename)



# -----------------------------------------------------------------------------
# High-level API of FreeType 2
# -----------------------------------------------------------------------------
FT_Init_FreeType       = __dll__.FT_Init_FreeType
FT_Done_FreeType       = __dll__.FT_Done_FreeType
FT_Library_Version     = __dll__.FT_Library_Version

def __del_library__(self):
    global __handle__
    if __handle__:
        try:
            FT_Done_FreeType(byref(self))
            __handle__ = None
        except:
            pass
FT_Library.__del__ = __del_library__

def get_handle():
    '''
    Get unique FT_Library handle
    '''
    global __handle__
    if not __handle__:
        __handle__ = FT_Library( )
        error = FT_Init_FreeType( byref(__handle__) )
        if error: raise FT_Exception(error)
        try:
            set_lcd_filter( FT_LCD_FILTER_DEFAULT )
        except:
            pass
        if error: raise FT_Exception(error)
    return __handle__

def version():
    '''
    Return the version of the FreeType library being used as a tuple of
    ( major version number, minor version number, patch version number )
    '''
    amajor = FT_Int()
    aminor = FT_Int()
    apatch = FT_Int()
    library = get_handle()
    FT_Library_Version(library, byref(amajor), byref(aminor), byref(apatch))
    return (amajor.value, aminor.value, apatch.value)

FT_Get_X11_Font_Format = __dll__.FT_Get_X11_Font_Format
FT_Get_X11_Font_Format.restype = c_char_p

FT_Library_SetLcdFilter= __dll__.FT_Library_SetLcdFilter
if version()>=(2,4,0):
    FT_Library_SetLcdFilterWeights = __dll__.FT_Library_SetLcdFilterWeights
FT_New_Face            = __dll__.FT_New_Face
FT_New_Memory_Face     = __dll__.FT_New_Memory_Face
FT_Open_Face           = __dll__.FT_Open_Face
FT_Attach_File         = __dll__.FT_Attach_File
FT_Attach_Stream       = __dll__.FT_Attach_Stream
if version()>=(2,4,2):
    FT_Reference_Face      = __dll__.FT_Reference_Face
FT_Done_Face           = __dll__.FT_Done_Face
FT_Done_Glyph          = __dll__.FT_Done_Glyph
FT_Select_Size         = __dll__.FT_Select_Size
FT_Request_Size        = __dll__.FT_Request_Size
FT_Set_Char_Size       = __dll__.FT_Set_Char_Size
FT_Set_Pixel_Sizes     = __dll__.FT_Set_Pixel_Sizes
FT_Load_Glyph          = __dll__.FT_Load_Glyph
FT_Load_Char           = __dll__.FT_Load_Char
FT_Set_Transform       = __dll__.FT_Set_Transform
FT_Render_Glyph        = __dll__.FT_Render_Glyph
FT_Get_Kerning         = __dll__.FT_Get_Kerning
FT_Get_Track_Kerning   = __dll__.FT_Get_Track_Kerning
FT_Get_Glyph_Name      = __dll__.FT_Get_Glyph_Name
FT_Get_Glyph           = __dll__.FT_Get_Glyph

FT_Glyph_Get_CBox      = __dll__.FT_Glyph_Get_CBox

FT_Get_Postscript_Name = __dll__.FT_Get_Postscript_Name
FT_Get_Postscript_Name.restype = c_char_p
FT_Select_Charmap      = __dll__.FT_Select_Charmap
FT_Set_Charmap         = __dll__.FT_Set_Charmap
FT_Get_Charmap_Index   = __dll__.FT_Get_Charmap_Index
FT_Get_CMap_Language_ID= __dll__.FT_Get_CMap_Language_ID
FT_Get_CMap_Format     = __dll__.FT_Get_CMap_Format
FT_Get_Char_Index      = __dll__.FT_Get_Char_Index
FT_Get_First_Char      = __dll__.FT_Get_First_Char
FT_Get_Next_Char       = __dll__.FT_Get_Next_Char
FT_Get_Name_Index      = __dll__.FT_Get_Name_Index
FT_Get_SubGlyph_Info   = __dll__.FT_Get_SubGlyph_Info
if version()>=(2,3,8):
    FT_Get_FSType_Flags    = __dll__.FT_Get_FSType_Flags
    FT_Get_FSType_Flags.restype  = c_ushort
FT_Get_Sfnt_Name_Count = __dll__.FT_Get_Sfnt_Name_Count
FT_Get_Sfnt_Name       = __dll__.FT_Get_Sfnt_Name

FT_Outline_GetInsideBorder  = __dll__.FT_Outline_GetInsideBorder
FT_Outline_GetOutsideBorder = __dll__.FT_Outline_GetOutsideBorder
FT_Outline_Get_BBox         = __dll__.FT_Outline_Get_BBox
FT_Outline_Get_CBox         = __dll__.FT_Outline_Get_CBox
FT_Stroker_New              = __dll__.FT_Stroker_New
FT_Stroker_Set              = __dll__.FT_Stroker_Set
FT_Stroker_Rewind           = __dll__.FT_Stroker_Rewind
FT_Stroker_ParseOutline     = __dll__.FT_Stroker_ParseOutline
FT_Stroker_BeginSubPath     = __dll__.FT_Stroker_BeginSubPath
FT_Stroker_EndSubPath       = __dll__.FT_Stroker_EndSubPath
FT_Stroker_LineTo           = __dll__.FT_Stroker_LineTo
FT_Stroker_ConicTo          = __dll__.FT_Stroker_ConicTo
FT_Stroker_CubicTo          = __dll__.FT_Stroker_CubicTo
FT_Stroker_GetBorderCounts  = __dll__.FT_Stroker_GetBorderCounts
FT_Stroker_ExportBorder     = __dll__.FT_Stroker_ExportBorder
FT_Stroker_GetCounts        = __dll__.FT_Stroker_GetCounts
FT_Stroker_Export           = __dll__.FT_Stroker_Export
FT_Stroker_Done             = __dll__.FT_Stroker_Done
FT_Glyph_Stroke             = __dll__.FT_Glyph_Stroke
FT_Glyph_StrokeBorder       = __dll__.FT_Glyph_StrokeBorder
FT_Glyph_To_Bitmap          = __dll__.FT_Glyph_To_Bitmap



# -----------------------------------------------------------------------------
#  Stand alone functions
# -----------------------------------------------------------------------------
def set_lcd_filter(filt):
    '''
    This function is used to apply color filtering to LCD decimated bitmaps,
    like the ones used when calling FT_Render_Glyph with FT_RENDER_MODE_LCD or
    FT_RENDER_MODE_LCD_V.

    Note:
    -----
    This feature is always disabled by default. Clients must make an explicit
    call to this function with a 'filter' value other than FT_LCD_FILTER_NONE
    in order to enable it.

    Due to PATENTS covering subpixel rendering, this function doesn't do
    anything except returning 'FT_Err_Unimplemented_Feature' if the
    configuration macro FT_CONFIG_OPTION_SUBPIXEL_RENDERING is not defined in
    your build of the library, which should correspond to all default builds of
    FreeType.

    The filter affects glyph bitmaps rendered through FT_Render_Glyph,
    FT_Outline_Get_Bitmap, FT_Load_Glyph, and FT_Load_Char.

    It does not affect the output of FT_Outline_Render and
    FT_Outline_Get_Bitmap.

    If this feature is activated, the dimensions of LCD glyph bitmaps are
    either larger or taller than the dimensions of the corresponding outline
    with regards to the pixel grid. For example, for FT_RENDER_MODE_LCD, the
    filter adds up to 3 pixels to the left, and up to 3 pixels to the right.

    The bitmap offset values are adjusted correctly, so clients shouldn't need
    to modify their layout and glyph positioning code when enabling the filter.
    '''
    library = get_handle()
    error = FT_Library_SetLcdFilter(library, filt)
    if error: raise FT_Exception(error)



def set_lcd_filter_weights(a,b,c,d,e):
    '''
    Use this function to override the filter weights selected by
    FT_Library_SetLcdFilter. By default, FreeType uses the quintuple (0x00,
    0x55, 0x56, 0x55, 0x00) for FT_LCD_FILTER_LIGHT, and (0x10, 0x40, 0x70,
    0x40, 0x10) for FT_LCD_FILTER_DEFAULT and FT_LCD_FILTER_LEGACY.

    Note:
    -----
    Only available if version > 2.4.0
    '''
    if version()>=(2,4,0):
        library = get_handle()
        weights = FT_Char(5)(a,b,c,d,e)
        error = FT_Library_SetLcdFilterWeights(library, weights)
        if error: raise FT_Exception(error)
    else:
        raise RuntimeError, \
              'set_lcd_filter_weights require freetype > 2.4.0'



# -----------------------------------------------------------------------------
#  Direct wrapper (simple renaming)
# -----------------------------------------------------------------------------
Vector = FT_Vector
Matrix = FT_Matrix



# -----------------------------------------------------------------------------
class BBox( object ):
    '''
    FT_BBox wrapper.

    A structure used to hold an outline's bounding box, i.e., the coordinates
    of its extrema in the horizontal and vertical directions.

    Note:
    -----
    The bounding box is specified with the coordinates of the lower left and
    the upper right corner. In PostScript, those values are often called
    (llx,lly) and (urx,ury), respectively.

    If 'yMin' is negative, this value gives the glyph's descender. Otherwise,
    the glyph doesn't descend below the baseline. Similarly, if 'ymax' is
    positive, this value gives the glyph's ascender.

    'xMin' gives the horizontal distance from the glyph's origin to the left
    edge of the glyph's bounding box. If 'xMin' is negative, the glyph
    extends to the left of the origin.
    '''

    def __init__(self, bbox):
        '''
        Create a new BBox object.

        Parameters:
        -----------
        bbox : a FT_BBox or a tuple of 4 values
        '''
        if type(bbox) is FT_BBox:
            self._FT_BBox = bbox
        else:
            self._FT_BBox = FT_BBox(*bbox)

    xMin = property(lambda self: self._FT_BBox.xMin,
                    doc = 'The horizontal minimum (left-most).')

    yMin = property(lambda self: self._FT_BBox.yMin,
                    doc = 'The vertical minimum (bottom-most).')

    xMax = property(lambda self: self._FT_BBox.xMax,
                    doc = 'The horizontal maximum (right-most).')

    yMax = property(lambda self: self._FT_BBox.yMax,
                    doc = 'The vertical maximum (top-most).')



# -----------------------------------------------------------------------------
class SizeMetrics( object ):
    '''
    The size metrics structure gives the metrics of a size object.

    Note:
    -----
    The scaling values, if relevant, are determined first during a size
    changing operation. The remaining fields are then set by the driver. For
    scalable formats, they are usually set to scaled values of the
    corresponding fields in Face.

    Note that due to glyph hinting, these values might not be exact for certain
    fonts. Thus they must be treated as unreliable with an error margin of at
    least one pixel!

    Indeed, the only way to get the exact metrics is to render all glyphs. As
    this would be a definite performance hit, it is up to client applications
    to perform such computations.

    The SizeMetrics structure is valid for bitmap fonts also.
    '''

    def __init__(self, metrics ):
        '''
        Create a new SizeMetrics object.

        Parameters:
        -----------
          metrics : a FT_SizeMetrics
        '''
        self._FT_Size_Metrics = metrics

    x_ppem = property( lambda self: self._FT_Size_Metrics.x_ppem,
       doc = '''The width of the scaled EM square in pixels, hence the term
                'ppem' (pixels per EM). It is also referred to as 'nominal
                width'.''' )

    y_ppem = property( lambda self: self._FT_Size_Metrics.y_ppem,
       doc = '''The height of the scaled EM square in pixels, hence the term
                'ppem' (pixels per EM). It is also referred to as 'nominal
                height'.''' )

    x_scale = property( lambda self: self._FT_Size_Metrics.x_scale,
        doc = '''A 16.16 fractional scaling value used to convert horizontal
                 metrics from font units to 26.6 fractional pixels. Only
                 relevant for scalable font formats.''' )

    y_scale = property( lambda self: self._FT_Size_Metrics.y_scale,
        doc = '''A 16.16 fractional scaling value used to convert vertical
                 metrics from font units to 26.6 fractional pixels. Only
                 relevant for scalable font formats.''' )

    ascender = property( lambda self: self._FT_Size_Metrics.ascender,
         doc = '''The ascender in 26.6 fractional pixels. See Face for the
                  details.''' )

    descender = property( lambda self: self._FT_Size_Metrics.descender,
          doc = '''The descender in 26.6 fractional pixels. See Face for the
                    details.''' )

    height = property( lambda self: self._FT_Size_Metrics.height,
       doc = '''The height in 26.6 fractional pixels. See Face for the details.''' )

    max_advance = property(lambda self: self._FT_Size_Metrics.max_advance,
            doc = '''The maximal advance width in 26.6 fractional pixels. See
                      Face for the details.''' )



# -----------------------------------------------------------------------------
class BitmapSize( object ):
    '''
    FT_Bitmap_Size wrapper

    This structure models the metrics of a bitmap strike (i.e., a set of glyphs
    for a given point size and resolution) in a bitmap font. It is used for the
    'available_sizes' field of Face.

    Note:
    -----
    Windows FNT: The nominal size given in a FNT font is not reliable. Thus
    when the driver finds it incorrect, it sets 'size' to some calculated
    values and sets 'x_ppem' and 'y_ppem' to the pixel width and height given
    in the font, respectively.

    TrueType embedded bitmaps: 'size', 'width', and 'height' values are not
    contained in the bitmap strike itself. They are computed from the global
    font parameters.
    '''
    def __init__(self, size ):
        '''
        Create a new SizeMetrics object.

        Parameters:
        -----------
        size : a FT_Bitmap_Size
        '''
        self._FT_Bitmap_Size = size

    height = property( lambda self: self._FT_Bitmap_Size.height,
       doc = '''The vertical distance, in pixels, between two consecutive
                baselines. It is always positive.''')

    width = property( lambda self: self._FT_Bitmap_Size.width,
      doc = '''The average width, in pixels, of all glyphs in the strike.''')

    size = property( lambda self: self._FT_Bitmap_Size.size,
     doc = '''The nominal size of the strike in 26.6 fractional points. This
              field is not very useful.''')

    x_ppem = property( lambda self: self._FT_Bitmap_Size.x_ppem,
       doc = '''The horizontal ppem (nominal width) in 26.6 fractional
                pixels.''')

    y_ppem = property( lambda self: self._FT_Bitmap_Size.y_ppem,
       doc = '''The vertical ppem (nominal width) in 26.6 fractional
                pixels.''')


# -----------------------------------------------------------------------------
class Bitmap(object):
    '''
    FT_Bitmap wrapper

    A structure used to describe a bitmap or pixmap to the raster. Note that we
    now manage pixmaps of various depths through the 'pixel_mode' field.

    Note:
    -----
    For now, the only pixel modes supported by FreeType are mono and
    grays. However, drivers might be added in the future to support more
    'colorful' options.
    '''
    def __init__(self, bitmap):
        '''
        Create a new Bitmap object.

        Parameters:
        -----------
        bitmap : a FT_Bitmap
        '''
        self._FT_Bitmap = bitmap

    rows = property(lambda self: self._FT_Bitmap.rows,
     doc = '''The number of bitmap rows.''')

    width = property(lambda self: self._FT_Bitmap.width,
      doc = '''The number of pixels in bitmap row.''')

    pitch = property(lambda self: self._FT_Bitmap.pitch,
      doc = '''The pitch's absolute value is the number of bytes taken by one
               bitmap row, including padding. However, the pitch is positive
               when the bitmap has a 'down' flow, and negative when it has an
               'up' flow. In all cases, the pitch is an offset to add to a
               bitmap pointer in order to go down one row.

               Note that 'padding' means the alignment of a bitmap to a byte
               border, and FreeType functions normally align to the smallest
               possible integer value.

               For the B/W rasterizer, 'pitch' is always an even number.

               To change the pitch of a bitmap (say, to make it a multiple of
               4), use FT_Bitmap_Convert. Alternatively, you might use callback
               functions to directly render to the application's surface; see
               the file 'example2.py' in the tutorial for a demonstration.''')

    def _get_buffer(self):
        data = [self._FT_Bitmap.buffer[i] for i in range(self.rows*self.pitch)]
        return data
    buffer = property(_get_buffer,
       doc = '''A typeless pointer to the bitmap buffer. This value should be
                aligned on 32-bit boundaries in most cases.''')

    num_grays = property(lambda self: self._FT_Bitmap.num_grays,
          doc = '''This field is only used with FT_PIXEL_MODE_GRAY; it gives
                   the number of gray levels used in the bitmap.''')

    pixel_mode = property(lambda self: self._FT_Bitmap.pixel_mode,
           doc = '''The pixel mode, i.e., how pixel bits are stored. See
                    FT_Pixel_Mode for possible values.''')
  
    palette_mode = property(lambda self: self._FT_Bitmap.palette_mode,
             doc ='''This field is intended for paletted pixel modes; it
                     indicates how the palette is stored. Not used currently.''')

    palette = property(lambda self: self._FT_Bitmap.palette,
        doc = '''A typeless pointer to the bitmap palette; this field is
                 intended for paletted pixel modes. Not used currently.''')




# -----------------------------------------------------------------------------
class Charmap( object ):
    '''
    FT_Charmap wrapper.

    A handle to a given character map. A charmap is used to translate character
    codes in a given encoding into glyph indexes for its parent's face. Some
    font formats may provide several charmaps per font.

    Each face object owns zero or more charmaps, but only one of them can be
    'active' and used by FT_Get_Char_Index or FT_Load_Char.

    The list of available charmaps in a face is available through the
    'face.num_charmaps' and 'face.charmaps' fields of FT_FaceRec.

    The currently active charmap is available as 'face.charmap'. You should
    call FT_Set_Charmap to change it.

    Note:
    -----
    When a new face is created (either through FT_New_Face or FT_Open_Face),
    the library looks for a Unicode charmap within the list and automatically
    activates it.

    See also:
    ---------
    See FT_CharMapRec for the publicly accessible fields of a given character
    map.
    '''

    def __init__( self, charmap ):
        '''
        Create a new Charmap object.

        Parameters:
        -----------
        charmap : a FT_Charmap
        '''
        self._FT_Charmap = charmap

    encoding = property( lambda self: self._FT_Charmap.contents.encoding,
         doc = '''An FT_Encoding tag identifying the charmap. Use this with
                  FT_Select_Charmap.''')

    platform_id = property( lambda self: self._FT_Charmap.contents.platform_id,
            doc = '''An ID number describing the platform for the following
                     encoding ID. This comes directly from the TrueType
                     specification and should be emulated for other
                     formats.''')

    encoding_id = property( lambda self: self._FT_Charmap.contents.encoding_id,
            doc = '''A platform specific encoding number. This also comes from
                     the TrueType specification and should be emulated
                     similarly.''')

    def _get_encoding_name(self):
        encoding = self.encoding
        for key,value in FT_ENCODINGS.items():
            if encoding == value:
                return key
        return 'Unknown encoding'
    encoding_name = property( _get_encoding_name,
              doc = '''A platform specific encoding name. This also comes from
                     the TrueType specification and should be emulated
                     similarly.''')

    def _get_index( self ):
        return FT_Get_Charmap_Index( self._FT_Charmap )
    index = property( _get_index,
      doc = '''The index into the array of character maps within the face to
               which 'charmap' belongs. If an error occurs, -1 is returned.''')

    def _get_cmap_language_id( self ):
        return FT_Get_CMap_Language_ID( self._FT_Charmap )
    cmap_language_id = property( _get_cmap_language_id,
                 doc = '''The language ID of 'charmap'. If 'charmap' doesn't
                          belong to a TrueType/sfnt face, just return 0 as the
                          default value.''')

    def _get_cmap_format( self ):
        return FT_Get_CMap_Format( self._FT_Charmap )
    cmap_format = property( _get_cmap_format,
            doc = '''The format of 'charmap'. If 'charmap' doesn't belong to a
                     TrueType/sfnt face, return -1.''')



# -----------------------------------------------------------------------------
class Outline( object ):
    '''
    FT_Outline wrapper.

    This structure is used to describe an outline to the scan-line converter.
    '''
    def __init__( self, outline ):
        '''
        Create a new Outline object.

        Parameters:
        -----------
        charmap : a FT_Outline
        '''
        self._FT_Outline = outline
        
    n_contours = property(lambda self: self._FT_Outline.n_contours)
    def _get_contours(self):
        n = self._FT_Outline.n_contours
        data = [self._FT_Outline.contours[i] for i in range(n)]
        return data
    contours = property(_get_contours,
         doc = '''The number of contours in the outline.''')

    n_points = property(lambda self: self._FT_Outline.n_points)
    def _get_points(self):
        n = self._FT_Outline.n_points
        data = []
        for i in range(n):
            v = self._FT_Outline.points[i]
            data.append( (v.x,v.y) )
        return data
    points = property( _get_points,
       doc = '''The number of points in the outline.''')

    def _get_tags(self):
        n = self._FT_Outline.n_points
        data = [self._FT_Outline.tags[i] for i in range(n)]
        return data
    tags = property(_get_tags,
     doc = '''A list of 'n_points' chars, giving each outline point's type.

              If bit 0 is unset, the point is 'off' the curve, i.e., a Bezier
              control point, while it is 'on' if set.

              Bit 1 is meaningful for 'off' points only. If set, it indicates a
              third-order Bezier arc control point; and a second-order control
              point if unset.

              If bit 2 is set, bits 5-7 contain the drop-out mode (as defined
              in the OpenType specification; the value is the same as the
              argument to the SCANMODE instruction).

              Bits 3 and 4 are reserved for internal purposes.''')
        
    flags = property(lambda self: self._FT_Outline.flags,
      doc = '''A set of bit flags used to characterize the outline and give
               hints to the scan-converter and hinter on how to
               convert/grid-fit it. See FT_OUTLINE_FLAGS.''')

    def get_inside_border( self ):
        '''
        Retrieve the FT_StrokerBorder value corresponding to the 'inside'
        borders of a given outline.

        Return:
        The border index. FT_STROKER_BORDER_RIGHT for empty or invalid
        outlines.
        '''
        return FT_Outline_GetInsideBorder( self._FT_Outline )

    def get_outside_border( self ):
        '''
        Retrieve the FT_StrokerBorder value corresponding to the 'outside'
        borders of a given outline.

        Return:
        The border index. FT_STROKER_BORDER_RIGHT for empty or invalid
        outlines.
        '''
        return FT_Outline_GetInsideBorder( self._FT_Outline )

    def get_bbox(self):
        '''
        Compute the exact bounding box of an outline. This is slower than
        computing the control box. However, it uses an advanced algorithm which
        returns very quickly when the two boxes coincide. Otherwise, the
        outline Bezier arcs are traversed to extract their extrema.
        '''
        bbox = FT_BBox()
        error = FT_Outline_Get_BBox(byref(self._FT_Outline), byref(bbox))
        if error: raise FT_Exception(error)
        return bbox

    def get_cbox(self):
        '''
        Return an outline's 'control box'. The control box encloses all the
        outline's points, including Bezier control points. Though it coincides
        with the exact bounding box for most glyphs, it can be slightly larger
        in some situations (like when rotating an outline which contains Bezier
        outside arcs).

        Computing the control box is very fast, while getting the bounding box
        can take much more time as it needs to walk over all segments and arcs
        in the outline. To get the latter, you can use the 'ftbbox' component
        which is dedicated to this single task.
        '''
        bbox = FT_BBox()
        error = FT_Outline_Get_CBox(byref(self._FT_Outline), byref(bbox))
        if error: raise FT_Exception(error)
        return BBox(bbox)




# -----------------------------------------------------------------------------
class Glyph( object ):
    '''
    FT_Glyph wrapper.

    The root glyph structure contains a given glyph image plus its advance
    width in 16.16 fixed float format.
    '''
    def __init__( self, glyph ):
        '''
        Create Glyph object from an FT glyph.

        Parameters:
        -----------
          glyph: valid FT_Glyph object
        '''
        self._FT_Glyph = glyph

    def __del__( self ):
        '''
        Destroy glyph.
        '''
        FT_Done_Glyph( self._FT_Glyph )

    def _get_format( self ):
        return self._FT_Glyph.contents.format
    format = property( _get_format,
       doc = '''The format of the glyph's image.''')


    def stroke( self, stroker, destroy=False ):
        '''
        Stroke a given outline glyph object with a given stroker.

        Parameters:
        -----------
          stroker: A stroker handle.

          destroy: A Boolean. If 1, the source glyph object is destroyed on
                   success.
        Note:
        -----
        The source glyph is untouched in case of error.
        '''
        error = FT_Glyph_Stroke( byref(self._FT_Glyph),
                                 stroker._FT_Stroker, destroy )
        if error: raise FT_Exception( error )

    def to_bitmap( self, mode, origin, destroy=False ):
        '''
        Convert a given glyph object to a bitmap glyph object.

        Parameters:
        -----------
        mode: An enumeration that describes how the data is rendered.

        origin: A pointer to a vector used to translate the glyph image
                before rendering. Can be 0 (if no translation). The origin is
                expressed in 26.6 pixels.

        destroy: A boolean that indicates that the original glyph image
                 should be destroyed by this function. It is never destroyed
                 in case of error.

        Note:
        -----
        This function does nothing if the glyph format isn't scalable.

        The glyph image is translated with the 'origin' vector before
        rendering.

        The first parameter is a pointer to an FT_Glyph handle, that will be
        replaced by this function (with newly allocated data). Typically, you
        would use (omitting error handling):
        '''
        error = FT_Glyph_To_Bitmap( byref(self._FT_Glyph),
                                    mode, origin, destroy)
        if error: raise FT_Exception( error )
        return BitmapGlyph( self._FT_Glyph )

    def get_cbox(self, bbox_mode):
        '''
        Return an outline's 'control box'. The control box encloses all the
        outline's points, including Bezier control points. Though it coincides
        with the exact bounding box for most glyphs, it can be slightly larger
        in some situations (like when rotating an outline which contains Bezier
        outside arcs).

        Computing the control box is very fast, while getting the bounding box
        can take much more time as it needs to walk over all segments and arcs
        in the outline. To get the latter, you can use the 'ftbbox' component
        which is dedicated to this single task.

        Parameters:
        -----------

        mode : The mode which indicates how to interpret the returned bounding
               box values.

        Note:
        -----

        Coordinates are relative to the glyph origin, using the y upwards
        convention.

        If the glyph has been loaded with FT_LOAD_NO_SCALE, 'bbox_mode' must be
        set to FT_GLYPH_BBOX_UNSCALED to get unscaled font units in 26.6 pixel
        format. The value FT_GLYPH_BBOX_SUBPIXELS is another name for this
        constant.

        Note that the maximum coordinates are exclusive, which means that one
        can compute the width and height of the glyph image (be it in integer
        or 26.6 pixels) as:

        width  = bbox.xMax - bbox.xMin;                                  
        height = bbox.yMax - bbox.yMin;                                  

        Note also that for 26.6 coordinates, if 'bbox_mode' is set to
        FT_GLYPH_BBOX_GRIDFIT, the coordinates will also be grid-fitted, which
        corresponds to:

        bbox.xMin = FLOOR(bbox.xMin);
        bbox.yMin = FLOOR(bbox.yMin);                                    
        bbox.xMax = CEILING(bbox.xMax);                                  
        bbox.yMax = CEILING(bbox.yMax);                                  
        
        To get the bbox in pixel coordinates, set 'bbox_mode' to
        FT_GLYPH_BBOX_TRUNCATE.

        To get the bbox in grid-fitted pixel coordinates, set 'bbox_mode' to
        FT_GLYPH_BBOX_PIXELS.
        '''
        bbox = FT_BBox()
        error = FT_Glyph_Get_CBox(byref(self._FT_Glyph), bbox_mode,byref(bbox))
        if error: raise FT_Exception(error)
        return BBox(bbox)



# -----------------------------------------------------------------------------
class BitmapGlyph( object ):
    '''
    FT_BitmapGlyph wrapper.

    A structure used for bitmap glyph images. This really is a 'sub-class' of
    FT_GlyphRec.
    '''
    def __init__( self, glyph ):
        '''
        Create Glyph object from an FT glyph.

        Parameters:
        -----------
          glyph: valid FT_Glyph object
        '''
        self._FT_BitmapGlyph = cast(glyph, FT_BitmapGlyph)

    # def __del__( self ):
    #     '''
    #     Destroy glyph.
    #     '''
    #     FT_Done_Glyph( cast(self._FT_BitmapGlyph, FT_Glyph) )


    def _get_format( self ):
        return self._FT_BitmapGlyph.contents.format
    format = property( _get_format,
       doc = '''The format of the glyph's image.''')


    def _get_bitmap( self ):
        return Bitmap( self._FT_BitmapGlyph.contents.bitmap )
    bitmap = property( _get_bitmap,
       doc = '''A descriptor for the bitmap.''')


    def _get_left( self ):
        return self._FT_BitmapGlyph.contents.left
    left = property( _get_left,
     doc = '''The left-side bearing, i.e., the horizontal distance from the
              current pen position to the left border of the glyph bitmap.''')


    def _get_top( self ):
        return self._FT_BitmapGlyph.contents.top
    top = property( _get_top,
    doc = '''The top-side bearing, i.e., the vertical distance from the
             current pen position to the top border of the glyph bitmap.
             This distance is positive for upwards y!''')


# -----------------------------------------------------------------------------
class GlyphSlot( object ):
    '''
    FT_GlyphSlot wrapper.

    FreeType root glyph slot class structure. A glyph slot is a container where
    individual glyphs can be loaded, be they in outline or bitmap format.
    '''

    def __init__( self, slot ):
        '''
        Create GlyphSlot object from an FT glyph slot.

        Parameters:
        -----------
          glyph: valid FT_GlyphSlot object
        '''
        self._FT_GlyphSlot = slot

    def get_glyph( self ):
        '''
        A function used to extract a glyph image from a slot. Note that the
        created FT_Glyph object must be released with FT_Done_Glyph.
        '''
        aglyph = FT_Glyph()
        error = FT_Get_Glyph( self._FT_GlyphSlot, byref(aglyph) )
        if error: raise FT_Exception( error )
        return Glyph( aglyph )

    def _get_bitmap( self ):
        return Bitmap( self._FT_GlyphSlot.contents.bitmap )
    bitmap = property( _get_bitmap,
       doc = '''This field is used as a bitmap descriptor when the slot format
                is FT_GLYPH_FORMAT_BITMAP. Note that the address and content of
                the bitmap buffer can change between calls of FT_Load_Glyph and
                a few other functions.''')

    def _get_next( self ):
        return GlyphSlot( self._FT_GlyphSlot.contents.next )
    next = property( _get_next,
     doc = '''In some cases (like some font tools), several glyph slots per
              face object can be a good thing. As this is rare, the glyph slots
              are listed through a direct, single-linked list using its 'next'
              field.''')

    advance = property( lambda self: self._FT_GlyphSlot.contents.advance,
        doc = '''This shorthand is, depending on FT_LOAD_IGNORE_TRANSFORM, the
                 transformed advance width for the glyph (in 26.6 fractional
                 pixel format). As specified with FT_LOAD_VERTICAL_LAYOUT, it
                 uses either the 'horiAdvance' or the 'vertAdvance' value of
                 'metrics' field.''')

    def _get_outline( self ):
        return Outline( self._FT_GlyphSlot.contents.outline )
    outline = property( _get_outline,
        doc = '''The outline descriptor for the current glyph image if its
                 format is FT_GLYPH_FORMAT_OUTLINE. Once a glyph is loaded,
                 'outline' can be transformed, distorted, embolded,
                 etc. However, it must not be freed.''')

    format = property( lambda self: self._FT_GlyphSlot.contents.format,
       doc = '''This field indicates the format of the image contained in the
                glyph slot. Typically FT_GLYPH_FORMAT_BITMAP,
                FT_GLYPH_FORMAT_OUTLINE, or FT_GLYPH_FORMAT_COMPOSITE, but
                others are possible.''')

    bitmap_top  = property( lambda self:
                             self._FT_GlyphSlot.contents.bitmap_top,
            doc = '''This is the bitmap's top bearing expressed in integer
                     pixels. Remember that this is the distance from the
                     baseline to the top-most glyph scanline, upwards y
                     coordinates being positive.''')

    bitmap_left = property( lambda self:
                            self._FT_GlyphSlot.contents.bitmap_left,
            doc = '''This is the bitmap's left bearing expressed in integer
                     pixels. Of course, this is only valid if the format is
                     FT_GLYPH_FORMAT_BITMAP.''')

    linearHoriAdvance = property( lambda self:
                                  self._FT_GlyphSlot.contents.linearHoriAdvance,
                  doc = '''The advance width of the unhinted glyph. Its value
                           is expressed in 16.16 fractional pixels, unless
                           FT_LOAD_LINEAR_DESIGN is set when loading the glyph.
                           This field can be important to perform correct
                           WYSIWYG layout. Only relevant for outline glyphs.''')

    linearVertAdvance = property( lambda self:
                                  self._FT_GlyphSlot.contents.linearVertAdvance,
                  doc = '''The advance height of the unhinted glyph. Its value
                           is expressed in 16.16 fractional pixels, unless
                           FT_LOAD_LINEAR_DESIGN is set when loading the glyph.
                           This field can be important to perform correct
                           WYSIWYG layout. Only relevant for outline glyphs.''')


# -----------------------------------------------------------------------------
#  Face wrapper
# -----------------------------------------------------------------------------
class Face( object ):
    '''
    FT_Face wrapper

    FreeType root face class structure. A face object models a typeface in a
    font file.
    '''
    def __init__( self, filename, index = 0 ):
        '''
        Build a new Face

        Parameters:
        -----------
        filename: A path to the font file.

        index: The index of the face within the font.
               The first face has index 0.
        '''
        library = get_handle( )
        face = FT_Face( )
        self._FT_Face = None
        u_filename = c_char_p(filename)
        error = FT_New_Face( library, u_filename, 0, byref(face) )
        if error: raise FT_Exception( error )
        self._filename = filename
        self._index = index
        self._FT_Face = face
    
    def __del__( self ):
        '''
        Discard  face object, as well as all of its child slots and sizes.
        '''
        if self._FT_Face is not None:
            FT_Done_Face( self._FT_Face )

    def get_format(self):
        '''
        Return a string describing the format of a given face, using values
        which can be used as an X11 FONT_PROPERTY. Possible values are
        ‘TrueType’, ‘Type 1’, ‘BDF’, ‘PCF’, ‘Type 42’, ‘CID Type 1’, ‘CFF’,
        ‘PFR’, and ‘Windows FNT’.
        '''
        
        return FT_Get_X11_Font_Format(self._FT_Face)

    def get_fstype(self):
        '''
        Return the fsType flags for a font (embedding permissions).

        The return value is a tuple containing the freetype enum name
        as a string and the actual flag as an int
        '''

        flag = FT_Get_FSType_Flags(self._FT_Face)
        for k, v in FT_FSTYPE_XXX.items():
            if v == flag:
                return k, v

    def set_char_size( self, width=0, height=0, hres=72, vres=72 ):
        '''
        This function calls FT_Request_Size to request the nominal size (in
        points).
        
        Parameters:
        -----------
        width: The nominal width, in 26.6 fractional points.

        height: The nominal height, in 26.6 fractional points.

        hres: The horizontal resolution in dpi.

        vres: The vertical resolution in dpi.

        Note:
        -----
        If either the character width or height is zero, it is set equal to the
        other value.

        If either the horizontal or vertical resolution is zero, it is set
        equal to the other value.

        A character width or height smaller than 1pt is set to 1pt; if both
        resolution values are zero, they are set to 72dpi.

        Don't use this function if you are using the FreeType cache API.
        '''
        error = FT_Set_Char_Size( self._FT_Face, width, height, hres, vres )
        if error: raise FT_Exception( error)

    def set_pixel_sizes( self, width, height ):
        '''
        This function calls FT_Request_Size to request the nominal size (in
        pixels).

        Parameters:
        -----------
        width: The nominal width, in pixels.

        height: The nominal height, in pixels.
        '''
        error = FT_Set_Pixel_Sizes( self._FT_Face, width, height )
        if error: raise FT_Exception(error)

    def select_charmap( self, encoding ):
        '''
        Select a given charmap by its encoding tag (as listed in 'freetype.h').

        Note:
        -----
        This function returns an error if no charmap in the face corresponds to
        the encoding queried here.

        Because many fonts contain more than a single cmap for Unicode
        encoding, this function has some special code to select the one which
        covers Unicode best ('best' in the sense that a UCS-4 cmap is preferred
        to a UCS-2 cmap). It is thus preferable to FT_Set_Charmap in this case.
        '''
        error = FT_Select_Charmap( self._FT_Face, encoding )
        if error: raise FT_Exception(error)

    def set_charmap( self, charmap ):
        '''
        Select a given charmap for character code to glyph index mapping.

        Parameters:
        -----------
        charmap: A handle to the selected charmap.
        '''
        error = FT_Set_Charmap( self._FT_Face, charmap._FT_Charmap )
        if error : raise FT_Exception(error)

    def get_char_index( self, charcode ):
        '''
        Return the glyph index of a given character code. This function uses a
        charmap object to do the mapping.

        Parameters:
        -----------
        charcode: The character code.

        Note:
        -----
        If you use FreeType to manipulate the contents of font files directly,
        be aware that the glyph index returned by this function doesn't always
        correspond to the internal indices used within the file. This is done
        to ensure that value 0 always corresponds to the 'missing glyph'.
        '''
        if type( charcode ) in (str,unicode):
            charcode = ord( charcode )
        return FT_Get_Char_Index( self._FT_Face, charcode )

    def get_first_char( self ):
        '''
        This function is used to return the first character code in the current
        charmap of a given face. It also returns the corresponding glyph index.

        Return:
        -------
        Glyph index of first character code. 0 if charmap is empty.

        Note:
        -----
        You should use this function with get_next_char to be able to parse
        all character codes available in a given charmap. The code should look
        like this:

        Note that 'agindex' is set to 0 if the charmap is empty. The result
        itself can be 0 in two cases: if the charmap is empty or if the value 0
        is the first valid character code.
        '''
        agindex = FT_UInt()
        charcode = FT_Get_First_Char( self._FT_Face, byref(agindex) )
        return charcode, agindex.value

    def get_next_char( self, charcode, agindex ):
        '''
        This function is used to return the next character code in the current
        charmap of a given face following the value 'char_code', as well as the
        corresponding glyph index.

        Parameters:
        -----------
        charcode: The starting character code.

        agindex: Glyph index of next character code. 0 if charmap is empty.

        Note:
        -----
        You should use this function with FT_Get_First_Char to walk over all
        character codes available in a given charmap. See the note for this
        function for a simple code example.

        Note that 'agindex' is set to 0 when there are no more
        codes in the charmap.
        '''
        agindex = FT_UInt( agindex )
        charcode = FT_Get_Next_Char( self._FT_Face, charcode, byref(agindex) )
        return charcode, agindex.value

    def get_name_index( self, name ):
        '''
        Return the glyph index of a given glyph name. This function uses driver
        specific objects to do the translation.

        Parameters:
        -----------
        glyph_name: The glyph name.
        '''
        return FT_Get_Name_Index( self._FT_Face, name )

    def set_transform( self, matrix, delta ):
        '''
        A function used to set the transformation that is applied to glyph
        images when they are loaded into a glyph slot through FT_Load_Glyph.

        Parameters:
        -----------
        matrix: A pointer to the transformation's 2x2 matrix.
                Use 0 for the identity matrix.

        delta: A pointer to the translation vector.
               Use 0 for the null vector.

        Note:
        -----
        The transformation is only applied to scalable image formats after the
        glyph has been loaded. It means that hinting is unaltered by the
        transformation and is performed on the character size given in the last
        call to FT_Set_Char_Size or FT_Set_Pixel_Sizes.

        Note that this also transforms the 'face.glyph.advance'
        field, but not the values in 'face.glyph.metrics'.
        '''
        FT_Set_Transform( self._FT_Face,
                          byref(matrix), byref(delta) )

    def select_size( self, strike_index ):
        '''
        Select a bitmap strike.

        Parameters:
        -----------

        strike_index: The index of the bitmap strike in the
                      'available_sizes' field of Face object.
        '''
        error = FT_Select_Size( self._FT_Face, strike_index )
        if error: raise FT_Exception( error )

    def load_glyph( self, index, flags = FT_LOAD_RENDER ):
        '''
        A function used to load a single glyph into the glyph slot of a face
        object.

        Parameters:
        -----------
        index: The index of the glyph in the font file. For CID-keyed fonts
               (either in PS or in CFF format) this argument specifies the CID
               value.

        flags: A flag indicating what to load for this glyph. The FT_LOAD_XXX
               constants can be used to control the glyph loading process
               (e.g., whether the outline should be scaled, whether to load
               bitmaps or not, whether to hint the outline, etc).

        Note:
        -----
        The loaded glyph may be transformed. See FT_Set_Transform for the
        details.

        For subsetted CID-keyed fonts, 'FT_Err_Invalid_Argument' is returned
        for invalid CID values (this is, for CID values which don't have a
        corresponding glyph in the font). See the discussion of the
        FT_FACE_FLAG_CID_KEYED flag for more details.
        '''
        error = FT_Load_Glyph( self._FT_Face, index, flags )
        if error: raise FT_Exception( error )

    def load_char( self, char, flags = FT_LOAD_RENDER ):
        '''
        A function used to load a single glyph into the glyph slot of a face
        object, according to its character code.

        Parameters:
        -----------
        char: The glyph's character code, according to the current charmap used
              in the face.

        flags: A flag indicating what to load for this glyph. The FT_LOAD_XXX
               constants can be used to control the glyph loading process
               (e.g., whether the outline should be scaled, whether to load
               bitmaps or not, whether to hint the outline, etc).

        Note:
        -----
        This function simply calls FT_Get_Char_Index and FT_Load_Glyph.
        '''
        error = FT_Load_Char( self._FT_Face, ord(char), flags )
        if error: raise FT_Exception( error )

    def get_kerning( self, left, right, mode = FT_KERNING_DEFAULT ):
        '''
        Return the kerning vector between two glyphs of a same face.

        Parameters:
        -----------
        left: The index of the left glyph in the kern pair.
        
        right: The index of the right glyph in the kern pair.

        mode: See FT_Kerning_Mode for more information. Determines the scale
              and dimension of the returned kerning vector.

        Note:
        -----
        Only horizontal layouts (left-to-right & right-to-left) are supported
        by this method. Other layouts, or more sophisticated kernings, are out
        of the scope of this API function -- they can be implemented through
        format-specific interfaces.
        '''
        left_glyph = self.get_char_index( left )
        right_glyph = self.get_char_index( right )
        kerning = FT_Vector(0,0)
        error = FT_Get_Kerning( self._FT_Face,
                                left_glyph, right_glyph, mode, byref(kerning) )
        if error: raise FT_Exception( error )
        return kerning

    def _get_sfnt_name_count(self):
        return FT_Get_Sfnt_Name_Count( self._FT_Face )
    sfnt_name_count = property(_get_sfnt_name_count,
                doc = '''Number of name strings in the SFNT 'name' table.''')

    def get_sfnt_name( self, index ):
        '''
        Retrieve a string of the SFNT 'name' table for a given index

        Parameters:
        -----------
        index: The index of the 'name' string.

        Note:
        -----

        The 'string' array returned in the 'aname' structure is not
        null-terminated. The application should deallocate it if it is no
        longer in use.

        Use FT_Get_Sfnt_Name_Count to get the total number of available 'name'
        table entries, then do a loop until you get the right platform,
        encoding, and name ID.
        '''
        name = FT_SfntName( )
        error = FT_Get_Sfnt_Name( self._FT_Face, index, byref(name) )
        if error: raise FT_Exception( error )
        return SfntName( name )

    def _get_postscript_name( self ):
        return FT_Get_Postscript_Name( self._FT_Face )
    postscript_name = property( _get_postscript_name,
                doc = '''ASCII PostScript name of face, if available. This only
                         works with PostScript and TrueType fonts.''')

    def _has_horizontal( self ):
        return bool( self.face_flags & FT_FACE_FLAG_HORIZONTAL )
    has_horizontal = property( _has_horizontal,
               doc = '''True whenever a face object contains horizontal metrics
               (this is true for all font formats though).''')

    def _has_vertical( self ):
        return bool( self.face_flags & FT_FACE_FLAG_VERTICAL )
    has_vertical = property( _has_vertical,
             doc = '''True whenever a face object contains vertical metrics.''')

    def _has_kerning( self ):
        return bool( self.face_flags & FT_FACE_FLAG_KERNING )
    has_kerning = property( _has_kerning,
            doc = '''True whenever a face object contains kerning data that can
                     be accessed with FT_Get_Kerning.''')

    def _is_scalable( self ):
        return bool( self.face_flags & FT_FACE_FLAG_SCALABLE )
    is_scalable = property( _is_scalable,
            doc = '''true whenever a face object contains a scalable font face
                     (true for TrueType, Type 1, Type 42, CID, OpenType/CFF,
                     and PFR font formats.''')

    def _is_sfnt( self ):
        return bool( self.face_flags & FT_FACE_FLAG_SFNT )
    is_sfnt = property( _is_sfnt,
        doc = '''true whenever a face object contains a font whose format is
                 based on the SFNT storage scheme. This usually means: TrueType
                 fonts, OpenType fonts, as well as SFNT-based embedded bitmap
                 fonts.

                 If this macro is true, all functions defined in
                 FT_SFNT_NAMES_H and FT_TRUETYPE_TABLES_H are available.''')

    def _is_fixed_width( self ):
        return bool( self.face_flags & FT_FACE_FLAG_FIXED_WIDTH )
    is_fixed_width = property( _is_fixed_width,
               doc = '''True whenever a face object contains a font face that
                        contains fixed-width (or 'monospace', 'fixed-pitch',
                        etc.) glyphs.''')
    
    def _has_fixed_sizes( self ):
        return bool( self.face_flags & FT_FACE_FLAG_FIXED_SIZES )
    has_fixed_sizes = property( _has_fixed_sizes,
                doc = '''True whenever a face object contains some embedded
                bitmaps. See the 'available_sizes' field of the FT_FaceRec
                structure.''')

    def _has_glyph_names( self ):
        return bool( self.face_flags & FT_FACE_FLAG_GLYPH_NAMES )
    has_glyph_names = property( _has_glyph_names,
                doc = '''True whenever a face object contains some glyph names
                         that can be accessed through FT_Get_Glyph_Name.''')

    def _has_multiple_masters( self ):
        return bool( self.face_flags & FT_FACE_FLAG_MULTIPLE_MASTERS )
    has_multiple_masters = property( _has_multiple_masters,
                     doc = '''True whenever a face object contains some
                              multiple masters. The functions provided by
                              FT_MULTIPLE_MASTERS_H are then available to
                              choose the exact design you want.''')

    def _is_cid_keyed( self ):
        return bool( self.face_flags & FT_FACE_FLAG_CID_KEYED )
    is_cid_keyed = property( _is_cid_keyed,
             doc = '''True whenever a face object contains a CID-keyed
                      font. See the discussion of FT_FACE_FLAG_CID_KEYED for
                      more details.

                      If this macro is true, all functions defined in FT_CID_H
                      are available.''')

    def _is_tricky( self ):
        return bool( self.face_flags & FT_FACE_FLAG_TRICKY )
    is_tricky = property( _is_tricky,
          doc = '''True whenever a face represents a 'tricky' font. See the
                   discussion of FT_FACE_FLAG_TRICKY for more details.''')


    num_faces = property(lambda self: self._FT_Face.contents.num_faces,
          doc = '''The number of faces in the font file. Some font formats can
                   have multiple faces in a font file.''')

    face_index = property(lambda self: self._FT_Face.contents.face_index,
           doc = '''The index of the face in the font file. It is set to 0 if
                    there is only one face in the font file.''')

    face_flags = property(lambda self: self._FT_Face.contents.face_flags,
           doc = '''A set of bit flags that give important information about
                    the face; see FT_FACE_FLAG_XXX for the details.''')

    style_flags = property(lambda self: self._FT_Face.contents.style_flags,
            doc = '''A set of bit flags indicating the style of the face; see
                     FT_STYLE_FLAG_XXX for the details.''')

    num_glyphs = property(lambda self: self._FT_Face.contents.num_glyphs,
           doc = '''The number of glyphs in the face. If the face is scalable
           and has sbits (see 'num_fixed_sizes'), it is set to the number of
           outline glyphs.

           For CID-keyed fonts, this value gives the highest CID used in the
           font.''')

    family_name = property(lambda self: self._FT_Face.contents.family_name,
            doc = '''The face's family name. This is an ASCII string, usually
                     in English, which describes the typeface's family (like
                     'Times New Roman', 'Bodoni', 'Garamond', etc). This is a
                     least common denominator used to list fonts. Some formats
                     (TrueType & OpenType) provide localized and Unicode
                     versions of this string. Applications should use the
                     format specific interface to access them. Can be NULL
                     (e.g., in fonts embedded in a PDF file).''')

    style_name = property(lambda self: self._FT_Face.contents.style_name,
           doc = '''The face's style name. This is an ASCII string, usually in
                    English, which describes the typeface's style (like
                    'Italic', 'Bold', 'Condensed', etc). Not all font formats
                    provide a style name, so this field is optional, and can be
                    set to NULL. As for 'family_name', some formats provide
                    localized and Unicode versions of this string. Applications
                    should use the format specific interface to access them.''')

    num_fixed_sizes = property(lambda self: self._FT_Face.contents.num_fixed_sizes,
                doc = '''The number of bitmap strikes in the face. Even if the
                         face is scalable, there might still be bitmap strikes,
                         which are called 'sbits' in that case.''')

    def _get_available_sizes( self ):
        sizes = []
        n = self.num_fixed_sizes
        FT_sizes = self._FT_Face.contents.available_sizes
        for i in range(n):
            sizes.append( BitmapSize(FT_sizes[i]) )
        return sizes
    available_sizes = property(_get_available_sizes,
                doc = '''A list of FT_Bitmap_Size for all bitmap strikes in the
                face. It is set to NULL if there is no bitmap strike.''')

    num_charmaps = property(lambda self: self._FT_Face.contents.num_charmaps)
    def _get_charmaps( self ):
        charmaps = []
        n = self._FT_Face.contents.num_charmaps
        FT_charmaps = self._FT_Face.contents.charmaps
        for i in range(n):
            charmaps.append( Charmap(FT_charmaps[i]) )
        return charmaps
    charmaps = property(_get_charmaps,
         doc = '''A list of the charmaps of the face.''')

    #       ('generic', FT_Generic),

    def _get_bbox( self ):
        return BBox( self._FT_Face.contents.bbox )
    bbox = property( _get_bbox,
     doc = '''The font bounding box. Coordinates are expressed in font units
              (see 'units_per_EM'). The box is large enough to contain any
              glyph from the font. Thus, 'bbox.yMax' can be seen as the
              'maximal ascender', and 'bbox.yMin' as the 'minimal
              descender'. Only relevant for scalable formats.

              Note that the bounding box might be off by (at least) one pixel
              for hinted fonts. See FT_Size_Metrics for further discussion.''')

    units_per_EM = property(lambda self: self._FT_Face.contents.units_per_EM,
             doc = '''The number of font units per EM square for this
                      face. This is typically 2048 for TrueType fonts, and 1000
                      for Type 1 fonts. Only relevant for scalable formats.''')

    ascender = property(lambda self: self._FT_Face.contents.ascender,
         doc = '''The typographic ascender of the face, expressed in font
                  units. For font formats not having this information, it is
                  set to 'bbox.yMax'. Only relevant for scalable formats.''')

    descender = property(lambda self: self._FT_Face.contents.descender,
          doc = '''The typographic descender of the face, expressed in font
                   units. For font formats not having this information, it is
                   set to 'bbox.yMin'. Note that this field is usually
                   negative. Only relevant for scalable formats.''')

    height = property(lambda self: self._FT_Face.contents.height,
       doc = '''The height is the vertical distance between two consecutive
                baselines, expressed in font units. It is always positive. Only
                relevant for scalable formats.''')

    max_advance_width = property(lambda self: self._FT_Face.contents.max_advance_width,
                  doc = '''The maximal advance width, in font units, for all
                           glyphs in this face. This can be used to make word
                           wrapping computations faster. Only relevant for
                           scalable formats.''')

    max_advance_height = property(lambda self: self._FT_Face.contents.max_advance_height,
                   doc = '''The maximal advance height, in font units, for all
                            glyphs in this face. This is only relevant for
                            vertical layouts, and is set to 'height' for fonts
                            that do not provide vertical metrics. Only relevant
                            for scalable formats.''')

    underline_position = property(lambda self: self._FT_Face.contents.underline_position,
                   doc = '''The position, in font units, of the underline line
                            for this face. It is the center of the underlining
                            stem. Only relevant for scalable formats.''')

    underline_thickness = property(lambda self: self._FT_Face.contents.underline_thickness,
                    doc = '''The thickness, in font units, of the underline for
                             this face. Only relevant for scalable formats.''')


    def _get_glyph( self ):
        return GlyphSlot( self._FT_Face.contents.glyph )
    glyph = property( _get_glyph,
      doc = '''The face's associated glyph slot(s).''')

    def _get_size( self ):
        size = self._FT_Face.contents.size
        metrics = size.contents.metrics
        return SizeMetrics(metrics)
    size = property( _get_size,
     doc = '''The current active size for this face.''')

    def _get_charmap( self ):
        return Charmap( self._FT_Face.contents.charmap)
    charmap = property( _get_charmap,
        doc = '''The current active charmap for this face.''')



# -----------------------------------------------------------------------------
#  SfntName wrapper
# -----------------------------------------------------------------------------
class SfntName( object ):
    '''
    SfntName wrapper

    A structure used to model an SFNT 'name' table entry.
    '''
    def __init__(self, name):
        '''
        Create a new SfntName object.

        Parameters:
        -----------
        name : SFNT 'name' table entry.

        '''
        self._FT_SfntName = name

    platform_id = property(lambda self: self._FT_SfntName.platform_id,
            doc = '''The platform ID for 'string'.''')

    encoding_id = property(lambda self: self._FT_SfntName.encoding_id,
            doc = '''The encoding ID for 'string'.''')

    language_id = property(lambda self: self._FT_SfntName.language_id,
            doc = '''The language ID for 'string'.''')

    name_id = property(lambda self: self._FT_SfntName.name_id,
        doc = '''An identifier for 'string'.''')

    #string      = property(lambda self: self._FT_SfntName.string)

    string_len = property(lambda self: self._FT_SfntName.string_len,
           doc = '''The length of 'string' in bytes.''')

    def _get_string(self):
    #     #s = self._FT_SfntName
         s = string_at(self._FT_SfntName.string, self._FT_SfntName.string_len)
         return s
    #     #return s.decode('utf-16be', 'ignore')
    #     return s.decode('utf-8', 'ignore')
    #     #n = s.string_len
    #     #data = [s.string[i] for i in range(n)]
    #     #return data
    string = property(_get_string,
       doc = '''The 'name' string. Note that its format differs depending on
                the (platform,encoding) pair. It can be a Pascal String, a
                UTF-16 one, etc.

                Generally speaking, the string is not zero-terminated. Please
                refer to the TrueType specification for details.''')



# -----------------------------------------------------------------------------
class Stroker( object ):
    '''
    FT_Stroker wrapper

    This component generates stroked outlines of a given vectorial glyph. It
    also allows you to retrieve the 'outside' and/or the 'inside' borders of
    the stroke.

    This can be useful to generate 'bordered' glyph, i.e., glyphs displayed
    with a coloured (and anti-aliased) border around their shape.
    '''

    def __init__( self ):
        '''
        Create a new Stroker object.
        '''
        library = get_handle( )
        stroker = FT_Stroker( )
        error = FT_Stroker_New( library, byref(stroker) )
        if error: raise FT_Exception( error )
        self._FT_Stroker = stroker


    def __del__( self ):
        '''
        Destroy object.
        '''
        FT_Stroker_Done( self._FT_Stroker )


    def set( self, radius, line_cap, line_join, miter_limit ):
        '''
        Reset a stroker object's attributes.

        Parameters:
        -----------
        radius     : The border radius.

        line_cap   : The line cap style.

        line_join  : The line join style.

        miter_limit: The miter limit for the FT_STROKER_LINEJOIN_MITER
                     style, expressed as 16.16 fixed point value.

        Note:
        -----
        The radius is expressed in the same units as the outline
        coordinates.
        '''
        FT_Stroker_Set( self._FT_Stroker,
                        radius, line_cap, line_join, miter_limit )


    def rewind( self ):
        '''
        Reset a stroker object without changing its attributes. You should call
        this function before beginning a new series of calls to
        FT_Stroker_BeginSubPath or FT_Stroker_EndSubPath.
        '''
        FT_Stroker_Rewind( self._FT_Stroker )


    def parse_outline( self, outline, opened ):
        '''
        A convenience function used to parse a whole outline with the
        stroker. The resulting outline(s) can be retrieved later by functions
        like FT_Stroker_GetCounts and FT_Stroker_Export.

        Parameters:
        -----------
        outline: The source outline.

        opened : A boolean. If 1, the outline is treated as an open path
                 instead of a closed one.

        Note:
        -----
        If 'opened' is 0 (the default), the outline is treated as a closed
        path, and the stroker generates two distinct 'border' outlines.

        If 'opened' is 1, the outline is processed as an open path, and the
        stroker generates a single 'stroke' outline.

        This function calls 'rewind' automatically.
        '''
        error = FT_Stroker_ParseOutline( self._FT_Stroker, outline, opened)
        if error: raise FT_Exception( error )


    def begin_subpath( self, to, open_ ):
        '''
        Start a new sub-path in the stroker.

        Parameters:
        -----------
        to   : A pointer to the start vector.

        open_: A boolean. If 1, the sub-path is treated as an open one.

        Note:
        -----
        This function is useful when you need to stroke a path that is not
        stored as an 'Outline' object.
        '''
        error = FT_Stroker_BeginSubPath( self._FT_Stroker, to, open_ )
        if error: raise FT_Exception( error )

    
    def end_subpath( self ):
        '''
        Close the current sub-path in the stroker.

        Note:
        -----
        You should call this function after 'begin_subpath'. If the subpath
        was not 'opened', this function 'draws' a single line segment to the
        start position when needed.
        '''
        error = FT_Stroker_EndSubPath( self._FT_Stroker)
        if error: raise FT_Exception( error )

    
    def line_to( self, to ):
        '''
        'Draw' a single line segment in the stroker's current sub-path, from
        the last position.

        Parameters:
        -----------
        to: A pointer to the destination point.

        Note:
        -----
        You should call this function between 'begin_subpath' and
        'end_subpath'.
        '''
        error = FT_Stroker_LineTo( self._FT_Stroker, to )
        if error: raise FT_Exception( error )

        
    def conic_to( self, control, to ):
        '''
        'Draw' a single quadratic Bezier in the stroker's current sub-path,
        from the last position.

        Parameters:
        -----------
        control: A pointer to a Bezier control point.
        to     : A pointer to the destination point.

        Note:
        -----
        You should call this function between 'begin_subpath' and
        'end_subpath'.
        '''
        error = FT_Stroker_ConicTo( self._FT_Stroker, control, to )
        if error: raise FT_Exception( error )
        

    def cubic_to( self, control1, control2, to ):
        '''
        'Draw' a single quadratic Bezier in the stroker's current sub-path,
        from the last position.

        Parameters:
        -----------
        control1: A pointer to the first Bezier control point.

        control2: A pointer to second Bezier control point.

        to      : A pointer to the destination point.

        Note:
        -----

        You should call this function between 'begin_subpath' and
        'end_subpath'.
        '''
        error = FT_Stroker_CubicTo( self._FT_Stroker, control1, control2, to )
        if error: raise FT_Exception( error )
        
        
    def get_border_counts( self, border ):
        '''
        Call this function once you have finished parsing your paths with the
        stroker. It returns the number of points and contours necessary to
        export one of the 'border' or 'stroke' outlines generated by the
        stroker.
        
        Parameters:
        -----------
        border: The border index.

        Return:
        -------
        number of points, number of contours
        '''
        anum_points = FT_UInt()
        anum_contours = FT_UInt()
        error = FT_Stroker_GetBorderCounts( self._FT_Stroker, border,
                                    byref(anum_points), byref(anum_contours) )
        if error: raise FT_Exception( error )
        return anum_points.value, anum_contours.value
                                            

    def export_border( self , border, outline ):
        '''
        Call this function after 'get_border_counts' to export the
        corresponding border to your own 'Outline' structure.

        Note that this function appends the border points and contours to your
        outline, but does not try to resize its arrays.

        Parameters:
        -----------
        border:  The border index.

        outline: The target outline.
            
        Note:
        -----
        Always call this function after get_border_counts to get sure that
        there is enough room in your 'Outline' object to receive all new
        data.

        When an outline, or a sub-path, is 'closed', the stroker generates two
        independent 'border' outlines, named 'left' and 'right'

        When the outline, or a sub-path, is 'opened', the stroker merges the
        'border' outlines with caps. The 'left' border receives all points,
        while the 'right' border becomes empty.

        Use the function export instead if you want to retrieve all borders
        at once.
        '''
        FT_Stroker_ExportBorder( self._FT_Stroker, border, outline._FT_Outline )


    def get_counts( self ):
        '''
        Call this function once you have finished parsing your paths with the
        stroker. It returns the number of points and contours necessary to
        export all points/borders from the stroked outline/path.

        Return:
        -------
        number of points, number of contours
        '''

        anum_points = FT_UInt()
        anum_contours = FT_UInt()
        error = FT_Stroker_GetCounts( self._FT_Stroker,
                                      byref(anum_points), byref(anum_contours) )
        if error: raise FT_Exception( error )
        return anum_points.value, anum_contours.value


    def export( self, outline ):
        '''
        Call this function after get_border_counts to export all borders to
        your own 'Outline' structure.

        Note that this function appends the border points and contours to your
        outline, but does not try to resize its arrays.

        Parameters:
        -----------
        outline: The target outline.
        '''
        FT_Stroker_Export( self._FT_Stroker, outline._FT_Outline )
