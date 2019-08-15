from enum import IntEnum

from .Texture import Texture
from ..ResourceReader import ResourceReader


class Texture2D(Texture):
	def __init__(self, reader):
		super().__init__(reader = reader)
		version = self.version
		self.m_Width = reader.read_int()
		self.m_Height = reader.read_int()
		self.m_CompleteImageSize = reader.read_int()
		self.m_TextureFormat = TextureFormat(reader.read_int())
		if version[0] < 5 or (version[0] == 5 and version[1] < 2):  # 5.2 down
			self.m_MipMap = reader.read_boolean()
		else:
			self.m_MipCount = reader.read_int()
		self.m_IsReadable = reader.read_boolean()  # 2.6.0 and up
		self.m_ReadAllowed = reader.read_boolean()  # 3.0.0 - 5.4
		# bool m_StreamingMipmaps 2018.2 and up
		reader.align_stream()
		if version[0] > 2018 or (version[0] == 2018 and version[1] >= 2):  # 2018.2 and up
			self.m_StreamingMipmapsPriority = reader.read_int()
		self.m_ImageCount = reader.read_int()
		self.m_TextureDimension = reader.read_int()
		self.m_TextureSettings = GLTextureSettings(reader)
		if version[0] >= 3:  # 3.0 and up
			self.m_LightmapFormat = reader.read_int()
		if version[0] > 3 or (version[0] == 3 and version[1] >= 5):  # 3.5.0 and up
			self.m_ColorSpace = reader.read_int()
		image_data_size = reader.read_int()
		if image_data_size == 0 and ((version[0] == 5 and version[1] >= 3) or version[0] > 5):  # 5.3.0 and up
			m_StreamData = StreamingInfo(reader)
		
		if 'm_StreamData' in locals() and m_StreamData.path:
			resource_reader = ResourceReader(m_StreamData.path, self.assets_file, m_StreamData.offset, m_StreamData.size)
		else:
			resource_reader = ResourceReader(reader, reader.Position, image_data_size)
		self.image_data = resource_reader.get_data()


class StreamingInfo:
	def __init__(self, reader):
		self.offset = reader.read_u_int()
		self.size = reader.read_u_int()
		self.path = reader.read_aligned_string()


class GLTextureSettings:
	def __init__(self, reader):
		version = reader.version
		
		self.m_FilterMode = reader.read_int()
		self.m_Aniso = reader.read_int()
		self.m_MipBias = reader.read_float()
		if version[0] >= 2017:  # 2017.x and up
			self.m_WrapMode = reader.read_int()  # m_WrapU
			self.m_WrapV = reader.read_int()
			self.m_WrapW = reader.read_int()
		else:
			self.m_WrapMode = reader.read_int()


class TextureFormat(IntEnum):
	Alpha8 = 1,
	ARGB4444 = 2,
	RGB24 = 3,
	RGBA32 = 4,
	ARGB32 = 5,
	RGB565 = 7,
	R16 = 9,
	DXT1 = 6,
	DXT5 = 12,
	RGBA4444 = 13,
	BGRA32 = 14,
	RHalf = 15,
	RGHalf = 16,
	RGBAHalf = 17,
	RFloat = 18,
	RGFloat = 19,
	RGBAFloat = 20,
	YUY2 = 21,
	RGB9e5Float = 22,
	BC4 = 26,
	BC5 = 27,
	BC6H = 24,
	BC7 = 25,
	DXT1Crunched = 28,
	DXT5Crunched = 29,
	PVRTC_RGB2 = 30,
	PVRTC_RGBA2 = 31,
	PVRTC_RGB4 = 32,
	PVRTC_RGBA4 = 33,
	ETC_RGB4 = 34,
	ATC_RGB4 = 35,
	ATC_RGBA8 = 36,
	EAC_R = 41,
	EAC_R_SIGNED = 42,
	EAC_RG = 43,
	EAC_RG_SIGNED = 44,
	ETC2_RGB = 45,
	ETC2_RGBA1 = 46,
	ETC2_RGBA8 = 47,
	ASTC_RGB_4x4 = 48,
	ASTC_RGB_5x5 = 49,
	ASTC_RGB_6x6 = 50,
	ASTC_RGB_8x8 = 51,
	ASTC_RGB_10x10 = 52,
	ASTC_RGB_12x12 = 53,
	ASTC_RGBA_4x4 = 54,
	ASTC_RGBA_5x5 = 55,
	ASTC_RGBA_6x6 = 56,
	ASTC_RGBA_8x8 = 57,
	ASTC_RGBA_10x10 = 58,
	ASTC_RGBA_12x12 = 59,
	ETC_RGB4_3DS = 60,
	ETC_RGBA8_3DS = 61,
	RG16 = 62,
	R8 = 63,
	ETC_RGB4Crunched = 64,
	ETC2_RGBA8Crunched = 65
