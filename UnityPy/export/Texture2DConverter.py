from ..classes.Texture2D import TextureFormat
import struct
from enum import IntEnum
from PIL import Image, ImageOps
import math
from decrunch import File as CrunchFile

def int_to_byte(i : int):
	return struct.pack("I", i)

'''
internal static class NativeMethods
	[DllImport("PVRTexLibWrapper.dll", CallingConvention = CallingConvention.Cdecl)]
	public static extern bool DecompressPVR(byte[] data, IntPtr image)

	[DllImport("TextureConverterWrapper.dll", CallingConvention = CallingConvention.Cdecl)]
	public static extern bool Ponvert(byte[] data, int dataSize, int width, int height, int type, bool fixAlpha, IntPtr image)

	[DllImport("crunch.dll", CallingConvention = CallingConvention.Cdecl)]
	public static extern bool DecompressCRN(byte[] data, int dataSize, out IntPtr uncompressedData, out int uncompressedSize)

	[DllImport("crunchunity.dll", CallingConvention = CallingConvention.Cdecl)]
	public static extern bool DecompressUnityCRN(byte[] data, int dataSize, out IntPtr uncompressedData, out int uncompressedSize)

	[DllImport("texgenpack.dll", CallingConvention = CallingConvention.Cdecl)]
	public static extern void TexgenPackDecode(byte[] data, int self.texturetype, int width, int height, IntPtr image)

	[DllImport("astc.dll", CallingConvention = CallingConvention.Cdecl)]
	public static extern bool DecodeASTC(byte[] data, int width, int height, int blockwidth, int blockheight, IntPtr image)
'''
def BGRA32ToBitmap(self) -> Image:
	codec = "raw"
	args = (self.format.pixel_format,)
	return Image.frombytes(mode, (self.m_Width, self.m_Height), data, codec, args)

'''
private Bitmap RGB565ToBitmap()
	# stride = self.m_Width * 2 + self.m_Width * 2 % 4
	# 所以self.m_Width * 2不为4的倍数时，需要在每行补上相应的像素
	byte[] buff
	padding = self.m_Width * 2 % 4
	stride = self.m_Width * 2 + padding
	if padding != 0:
		buff = new byte[stride * self.m_Height]
		for (int i = 0 i < self.m_Height i++)
			Buffer.BlockCopy(self.image_data, i * self.m_Width * 2, buff, i * stride, self.m_Width * 2)
	else
		buff = self.image_data
	gch = GCHandle.Alloc(buff, GCHandleType.Pinned)
	imagePtr = gch.AddrOfPinnedObject()
	bitmap = new Bitmap(self.m_Width, self.m_Height, stride, PixelFormat.Format16bppRgb565, imagePtr)
	gch.Free()
	return bitmap

private Bitmap PVRToBitmap(byte[] pvrData)
	imageBuff = new byte[self.m_Width * self.m_Height * 4]
	gch = GCHandle.Alloc(imageBuff, GCHandleType.Pinned)
	imagePtr = gch.AddrOfPinnedObject()
	if !NativeMethods.DecompressPVR(pvrData, imagePtr):
		gch.Free()
		return null
	bitmap = new Bitmap(self.m_Width, self.m_Height, self.m_Width * 4, PixelFormat.Format32bppArgb, imagePtr)
	gch.Free()
	return bitmap

private Bitmap TextureConverter()
	imageBuff = new byte[self.m_Width * self.m_Height * 4]
	gch = GCHandle.Alloc(imageBuff, GCHandleType.Pinned)
	imagePtr = gch.AddrOfPinnedObject()
	fixAlpha = self.glBaseInternalFormat == KTXHeader.GL_RED or self.glBaseInternalFormat == KTXHeader.GL_RG
	if !NativeMethods.Ponvert(self.image_data, self.image_data_size, self.m_Width, self.m_Height, (int)self.q_format, fixAlpha, imagePtr):
		gch.Free()
		return null
	bitmap = new Bitmap(self.m_Width, self.m_Height, self.m_Width * 4, PixelFormat.Format32bppArgb, imagePtr)
	gch.Free()
	return bitmap
'''
def DecompressCRN(self):
	# IntPtr uncompressedData
	# int uncompressedSize
	# bool result
	# if self.version[0] > 2017 or (self.version[0] == 2017 and self.version[1] >= 3 # 2017.3 and up
	# 	or self.m_TextureFormat == TextureFormat.ETC_RGB4Crunched
	# 	or self.m_TextureFormat == TextureFormat.ETC2_RGBA8Crunched):
	# 	result = NativeMethods.DecompressUnityCRN(self.image_data, self.image_data_size, out uncompressedData, out uncompressedSize)
	# else
	# 	result = NativeMethods.DecompressCRN(self.image_data, self.image_data_size, out uncompressedData, out uncompressedSize)

	# if result:
	# 	uncompressedBytes = new byte[uncompressedSize]
	# 	Marshal.Copy(uncompressedData, uncompressedBytes, 0, uncompressedSize)
	# 	Marshal.FreeHGlobal(uncompressedData)
	self.image_data = CrunchFile(self.image_data).decode_level(0)
	self.image_data_size = len(self.image_data)

'''
private Bitmap TexgenPackDecode()
	imageBuff = new byte[self.m_Width * self.m_Height * 4]
	gch = GCHandle.Alloc(imageBuff, GCHandleType.Pinned)
	imagePtr = gch.AddrOfPinnedObject()
	NativeMethods.TexgenPackDecode(self.image_data, (int)self.texturetype, self.m_Width, self.m_Height, imagePtr)
	bitmap = new Bitmap(self.m_Width, self.m_Height, self.m_Width * 4, PixelFormat.Format32bppArgb, imagePtr)
	gch.Free()
	return bitmap

private Bitmap DecodeASTC()
	imageBuff = new byte[self.m_Width * self.m_Height * 4]
	gch = GCHandle.Alloc(imageBuff, GCHandleType.Pinned)
	imagePtr = gch.AddrOfPinnedObject()
	if !NativeMethods.DecodeASTC(self.image_data, self.m_Width, self.m_Height, self.astcBlockWidth, self.astcBlockHeight, imagePtr):
		gch.Free()
		return null
	bitmap = new Bitmap(self.m_Width, self.m_Height, self.m_Width * 4, PixelFormat.Format32bppArgb, imagePtr)
	gch.Free()
	return bitmap
'''

class Texture2DConverter:
	# default variables
	self.dwFlags = 0x1 + 0x2 + 0x4 + 0x1000
	self.dwMipMapCount = 0x1
	dwSize = 0x20
	self.dwCaps = 0x1000
	self.dwCaps2 = 0x0
	# DDS Start
	dwMagic = b'DDS |'
	# DDS End
	# PVR Start
	pvrself.version = b'PVR\x03'
	pvrFlags = 0x0
	pvrColourSpace = 0x0
	pvrChannelType = 0x0
	pvrDepth = 0x1
	pvrNumSurfaces = 0x1 # For texture arrays
	pvrNumFaces = 0x1 # For cube maps
	pvrMetaDataSize = 0x0
	# PVR End
	# KTX Start
	glType = 0
	glTypeSize = 1
	glFormat = 0
	pixelDepth = 0
	numberOfArrayElements = 0
	numberOfFaces = 1
	numberOfMipmapLevels = 1
	bytesOfKeyValueData = 0
	# KTX END
	# default variavbles end
		
	def __init__(self, m_Texture2D):
		self.image_data = m_Texture2D.image_data.Value
		self.image_data_size = len(self.image_data)
		self.m_Width = m_Texture2D.self.m_Width
		self.m_Height = m_Texture2D.self.m_Height
		self.m_TextureFormat = m_Texture2D.self.m_TextureFormat
		self.mMipMap = m_Texture2D.m_MipMap
		self.version = m_Texture2D.self.version
		self.platform = m_Texture2D.self.platform

		if self.version[0] < 5 or (self.version[0] == 5 and self.version[1] < 2):# 5.2 down
			if self.mMipMap:
				self.dwFlags += 0x20000
				self.dwMipMapCount = math.log(max(self.m_Width, self.m_Height) // math.log(2))
				self.dwCaps += 0x400008
		else:
			self.dwFlags += 0x20000
			self.dwMipMapCount = m_Texture2D.m_MipCount
			self.dwCaps += 0x400008


		# TODO 导出到DDS容器时应该用原像素还是转换以后的像素？
		if self.m_TextureFormat == TextureFormat.Alpha8: # test pass
				'''
				self.dwFlags2 = 0x2
				self.dwRGBBitCount = 0x8
				self.dwRBitMask = 0x0
				self.dwGBitMask = 0x0
				self.dwBBitMask = 0x0
				self.dwABitMask = 0xFF
				'''

				# 转BGRA32
				BGRA32 = [0xFF]*(self.image_data_size * 4)
				for i in range(self.image_data_size):
					BGRA32[i * 4 + 3] = self.image_data[i]
				self.SetBGRA32Info(BGRA32)

		if self.m_TextureFormat == TextureFormat.ARGB4444: # test pass
				self.SwapBytesForXbox(self.platform)

				'''
				self.dwFlags2 = 0x41
				self.dwRGBBitCount = 0x10
				self.dwRBitMask = 0xF00
				self.dwGBitMask = 0xF0
				self.dwBBitMask = 0xF
				self.dwABitMask = 0xF000
				'''

				# 转BGRA32
				BGRA32 = bytearray(self.image_data_size * 2)
				for i in range(self.image_data_size / 2):
					pixelNew = new byte[4]
					pixelOldShort = BitConverter.ToUInt16(self.image_data, i * 2)
					pixelNew[0] = (byte)(pixelOldShort & 0x000f)
					pixelNew[1] = (byte)((pixelOldShort & 0x00f0) >> 4)
					pixelNew[2] = (byte)((pixelOldShort & 0x0f00) >> 8)
					pixelNew[3] = (byte)((pixelOldShort & 0xf000) >> 12)
					#  convert range
					for (j = 0 j < 4 j++)
						pixelNew[j] = (byte)((pixelNew[j] << 4) | pixelNew[j])
					pixelNew.CopyTo(BGRA32, i * 4)
				self.SetBGRA32Info(BGRA32)

		elif self.m_TextureFormat == TextureFormat.RGB24: # test pass
				'''
				self.dwFlags2 = 0x40
				self.dwRGBBitCount = 0x18
				self.dwRBitMask = 0xFF
				self.dwGBitMask = 0xFF00
				self.dwBBitMask = 0xFF0000
				self.dwABitMask = 0x0
				'''

				# 转BGRA32
				BGRA32 = new byte[self.image_data_size / 3 * 4]
				for i in range(self.image_data_size / 3):
					BGRA32[i * 4] = self.image_data[i * 3 + 2]
					BGRA32[i * 4 + 1] = self.image_data[i * 3 + 1]
					BGRA32[i * 4 + 2] = self.image_data[i * 3 + 0]
					BGRA32[i * 4 + 3] = 255
				self.SetBGRA32Info(BGRA32)

		elif self.m_TextureFormat == TextureFormat.RGBA32: # test pass
				'''
				self.dwFlags2 = 0x41
				self.dwRGBBitCount = 0x20
				self.dwRBitMask = 0xFF
				self.dwGBitMask = 0xFF00
				self.dwBBitMask = 0xFF0000
				self.dwABitMask = -16777216
				'''

				# 转BGRA32
				BGRA32 = new byte[self.image_data_size]
				for (i = 0 i < self.image_data_size i += 4)
					BGRA32[i] = self.image_data[i + 2]
					BGRA32[i + 1] = self.image_data[i + 1]
					BGRA32[i + 2] = self.image_data[i + 0]
					BGRA32[i + 3] = self.image_data[i + 3]
				self.SetBGRA32Info(BGRA32)

		elif self.m_TextureFormat == TextureFormat.ARGB32:# test pass
				'''
				self.dwFlags2 = 0x41
				self.dwRGBBitCount = 0x20
				self.dwRBitMask = 0xFF00
				self.dwGBitMask = 0xFF0000
				self.dwBBitMask = -16777216
				self.dwABitMask = 0xFF
				'''

				# 转BGRA32
				BGRA32 = new byte[self.image_data_size]
				for (i = 0 i < self.image_data_size i += 4)
					BGRA32[i] = self.image_data[i + 3]
					BGRA32[i + 1] = self.image_data[i + 2]
					BGRA32[i + 2] = self.image_data[i + 1]
					BGRA32[i + 3] = self.image_data[i + 0]
				self.SetBGRA32Info(BGRA32)

		elif self.m_TextureFormat == TextureFormat.RGB565: # test pass
				self.SwapBytesForXbox(self.platform)

				self.dwFlags2 = 0x40
				self.dwRGBBitCount = 0x10
				self.dwRBitMask = 0xF800
				self.dwGBitMask = 0x7E0
				self.dwBBitMask = 0x1F
				self.dwABitMask = 0x0

		elif self.m_TextureFormat == TextureFormat.R16: # test pass
				# 转BGRA32
				BGRA32 = new byte[self.image_data_size * 2]
				for (i = 0 i < self.image_data_size i += 2)
					float f = Half.ToHalf(self.image_data, i)
					BGRA32[i * 2 + 2] = (byte)Math.Ceiling(f * 255)# R
					BGRA32[i * 2 + 3] = 255# A
				self.SetBGRA32Info(BGRA32)

		elif self.m_TextureFormat in [
				TextureFormat.DXT1, # test pass
				TextureFormat.DXT1Crunched # test pass
			]:
				self.SwapBytesForXbox(self.platform)

				if self.mMipMap:
					dwPitchOrLinearSize = self.m_Height * self.m_Width / 2
				self.dwFlags2 = 0x4
				self.dwFourCC = 0x31545844
				self.dwRGBBitCount = 0x0
				self.dwRBitMask = 0x0
				self.dwGBitMask = 0x0
				self.dwBBitMask = 0x0
				self.dwABitMask = 0x0

				self.q_format = QFORMAT.self.q_format_S3TC_DXT1_RGB

		elif self.m_TextureFormat in [
				TextureFormat.DXT5, # test pass
				TextureFormat.DXT5Crunched # test pass
			]:
				self.SwapBytesForXbox(self.platform)

				if self.mMipMap:
					dwPitchOrLinearSize = self.m_Height * self.m_Width / 2
				self.dwFlags2 = 0x4
				self.dwFourCC = 0x35545844
				self.dwRGBBitCount = 0x0
				self.dwRBitMask = 0x0
				self.dwGBitMask = 0x0
				self.dwBBitMask = 0x0
				self.dwABitMask = 0x0

				self.q_format = QFORMAT.self.q_format_S3TC_DXT5_RGBA

		elif self.m_TextureFormat == TextureFormat.RGBA4444: # test pass
				'''
				self.dwFlags2 = 0x41
				self.dwRGBBitCount = 0x10
				self.dwRBitMask = 0xF000
				self.dwGBitMask = 0xF00
				self.dwBBitMask = 0xF0
				self.dwABitMask = 0xF
				'''

				# 转BGRA32
				BGRA32 = new byte[self.image_data_size * 2]
				for i in range(self.image_data_size / 2):
					pixelNew = new byte[4]
					pixelOldShort = BitConverter.ToUInt16(self.image_data, i * 2)
					pixelNew[0] = (byte)((pixelOldShort & 0x00f0) >> 4)
					pixelNew[1] = (byte)((pixelOldShort & 0x0f00) >> 8)
					pixelNew[2] = (byte)((pixelOldShort & 0xf000) >> 12)
					pixelNew[3] = (byte)(pixelOldShort & 0x000f)
					#  convert range
					for (j = 0 j < 4 j++)
						pixelNew[j] = (byte)((pixelNew[j] << 4) | pixelNew[j])
					pixelNew.CopyTo(BGRA32, i * 4)
				self.SetBGRA32Info(BGRA32)

		elif self.m_TextureFormat == TextureFormat.BGRA32: # test pass
				self.dwFlags2 = 0x41
				self.dwRGBBitCount = 0x20
				self.dwRBitMask = 0xFF0000
				self.dwGBitMask = 0xFF00
				self.dwBBitMask = 0xFF
				self.dwABitMask = -16777216

		elif self.m_TextureFormat == TextureFormat.RHalf: # test pass
				self.q_format = QFORMAT.self.q_format_R_16F
				self.glInternalFormat = KTXHeader.GL_R16F
				self.glBaseInternalFormat = KTXHeader.GL_RED

		elif self.m_TextureFormat == TextureFormat.RGHalf: # test pass
				self.q_format = QFORMAT.self.q_format_RG_HF
				self.glInternalFormat = KTXHeader.GL_RG16F
				self.glBaseInternalFormat = KTXHeader.GL_RG

		elif self.m_TextureFormat == TextureFormat.RGBAHalf: # test pass
				self.q_format = QFORMAT.self.q_format_RGBA_HF
				self.glInternalFormat = KTXHeader.GL_RGBA16F
				self.glBaseInternalFormat = KTXHeader.GL_RGBA

		elif self.m_TextureFormat == TextureFormat.RFloat: # test pass
				self.q_format = QFORMAT.self.q_format_R_F
				self.glInternalFormat = KTXHeader.GL_R32F
				self.glBaseInternalFormat = KTXHeader.GL_RED

		elif self.m_TextureFormat == TextureFormat.RGFloat: # test pass
				self.q_format = QFORMAT.self.q_format_RG_F
				self.glInternalFormat = KTXHeader.GL_RG32F
				self.glBaseInternalFormat = KTXHeader.GL_RG

		elif self.m_TextureFormat == TextureFormat.RGBAFloat: # test pass
				self.q_format = QFORMAT.self.q_format_RGBA_F
				self.glInternalFormat = KTXHeader.GL_RGBA32F
				self.glBaseInternalFormat = KTXHeader.GL_RGBA

		elif self.m_TextureFormat == TextureFormat.YUY2: # test pass
				self.pvrPixelFormat = 17

		elif self.m_TextureFormat == TextureFormat.RGB9e5Float: # TODO Test failure
				self.q_format = QFORMAT.self.q_format_RGB9_E5

		elif self.m_TextureFormat == TextureFormat.BC4: # test pass
				self.texturetype = texgenpack_self.texturetype.RGTC1
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RED_RGTC1
				self.glBaseInternalFormat = KTXHeader.GL_RED

		elif self.m_TextureFormat == TextureFormat.BC5: # test pass
				self.texturetype = texgenpack_self.texturetype.RGTC2
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RG_RGTC2
				self.glBaseInternalFormat = KTXHeader.GL_RG

		elif self.m_TextureFormat == TextureFormat.BC6H: # test pass
				self.texturetype = texgenpack_self.texturetype.BPTC_FLOAT
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT
				self.glBaseInternalFormat = KTXHeader.GL_RGB

		elif self.m_TextureFormat == TextureFormat.BC7: # test pass
				self.texturetype = texgenpack_self.texturetype.BPTC
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGBA_BPTC_UNORM
				self.glBaseInternalFormat = KTXHeader.GL_RGBA

		elif self.m_TextureFormat == TextureFormat.PVRTC_RGB2: # test pass
				self.pvrPixelFormat = 0
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGB_PVRTC_2BPPV1_IMG
				self.glBaseInternalFormat = KTXHeader.GL_RGB

		elif self.m_TextureFormat == TextureFormat.PVRTC_RGBA2: # test pass
				self.pvrPixelFormat = 1
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGBA_PVRTC_2BPPV1_IMG
				self.glBaseInternalFormat = KTXHeader.GL_RGBA

		elif self.m_TextureFormat == TextureFormat.PVRTC_RGB4: # test pass
				self.pvrPixelFormat = 2
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGB_PVRTC_4BPPV1_IMG
				self.glBaseInternalFormat = KTXHeader.GL_RGB

		elif self.m_TextureFormat == TextureFormat.PVRTC_RGBA4: # test pass
				self.pvrPixelFormat = 3
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGBA_PVRTC_4BPPV1_IMG
				self.glBaseInternalFormat = KTXHeader.GL_RGBA

		elif self.m_TextureFormat in [
				TextureFormat.ETC_RGB4Crunched, # test pass
				TextureFormat.ETC_RGB4_3DS, # test pass
				TextureFormat.ETC_RGB4 # test pass
			]:
				self.pvrPixelFormat = 6
				self.glInternalFormat = KTXHeader.GL_ETC1_RGB8_OES
				self.glBaseInternalFormat = KTXHeader.GL_RGB

		elif self.m_TextureFormat == TextureFormat.ATC_RGB4: # test pass
				self.q_format = QFORMAT.self.q_format_ATITC_RGB
				self.glInternalFormat = KTXHeader.GL_ATC_RGB_AMD
				self.glBaseInternalFormat = KTXHeader.GL_RGB

		elif self.m_TextureFormat == TextureFormat.ATC_RGBA8: # test pass
				self.q_format = QFORMAT.self.q_format_ATC_RGBA_INTERPOLATED_ALPHA
				self.glInternalFormat = KTXHeader.GL_ATC_RGBA_INTERPOLATED_ALPHA_AMD
				self.glBaseInternalFormat = KTXHeader.GL_RGBA

		elif self.m_TextureFormat == TextureFormat.EAC_R: # test pass
				self.q_format = QFORMAT.self.q_format_EAC_R_UNSIGNED
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_R11_EAC
				self.glBaseInternalFormat = KTXHeader.GL_RED

		elif self.m_TextureFormat == TextureFormat.EAC_R_SIGNED: # test pass
				self.q_format = QFORMAT.self.q_format_EAC_R_SIGNED
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_SIGNED_R11_EAC
				self.glBaseInternalFormat = KTXHeader.GL_RED

		elif self.m_TextureFormat == TextureFormat.EAC_RG: # test pass
				self.q_format = QFORMAT.self.q_format_EAC_RG_UNSIGNED
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RG11_EAC
				self.glBaseInternalFormat = KTXHeader.GL_RG

		elif self.m_TextureFormat == TextureFormat.EAC_RG_SIGNED: # test pass
				self.q_format = QFORMAT.self.q_format_EAC_RG_SIGNED
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_SIGNED_RG11_EAC
				self.glBaseInternalFormat = KTXHeader.GL_RG

		elif self.m_TextureFormat == TextureFormat.ETC2_RGB:  # test pass
				self.pvrPixelFormat = 22
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGB8_ETC2
				self.glBaseInternalFormat = KTXHeader.GL_RGB

		elif self.m_TextureFormat == TextureFormat.ETC2_RGBA1:  # test pass
				self.pvrPixelFormat = 24
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2
				self.glBaseInternalFormat = KTXHeader.GL_RGBA

		elif self.m_TextureFormat == TextureFormat.ETC2_RGBA8Crunched: # test pass
		elif self.m_TextureFormat == TextureFormat.ETC_RGBA8_3DS: # test pass
		elif self.m_TextureFormat == TextureFormat.ETC2_RGBA8:  # test pass
				self.pvrPixelFormat = 23
				self.glInternalFormat = KTXHeader.GL_COMPRESSED_RGBA8_ETC2_EAC
				self.glBaseInternalFormat = KTXHeader.GL_RGBA

		elif self.m_TextureFormat == TextureFormat.ASTC_RGB_4x4: # test pass
		elif self.m_TextureFormat == TextureFormat.ASTC_RGBA_4x4: # test pass
				self.astcBlockWidth = 4
				self.astcBlockHeight = 4

		elif self.m_TextureFormat == TextureFormat.ASTC_RGB_5x5: # test pass
		elif self.m_TextureFormat == TextureFormat.ASTC_RGBA_5x5: # test pass
				self.astcBlockWidth = 5
				self.astcBlockHeight = 5

		elif self.m_TextureFormat == TextureFormat.ASTC_RGB_6x6: # test pass
		elif self.m_TextureFormat == TextureFormat.ASTC_RGBA_6x6: # test pass
				self.astcBlockWidth = 6
				self.astcBlockHeight = 6

		elif self.m_TextureFormat == TextureFormat.ASTC_RGB_8x8: # test pass
		elif self.m_TextureFormat == TextureFormat.ASTC_RGBA_8x8: # test pass
				self.astcBlockWidth = 8
				self.astcBlockHeight = 8

		elif self.m_TextureFormat == TextureFormat.ASTC_RGB_10x10: # test pass
		elif self.m_TextureFormat == TextureFormat.ASTC_RGBA_10x10: # test pass
				self.astcBlockWidth = 10
				self.astcBlockHeight = 10

		elif self.m_TextureFormat == TextureFormat.ASTC_RGB_12x12: # test pass
		elif self.m_TextureFormat == TextureFormat.ASTC_RGBA_12x12: # test pass
				self.astcBlockWidth = 12
				self.astcBlockHeight = 12

		elif self.m_TextureFormat == TextureFormat.RG16: # test pass
				# 转BGRA32
				BGRA32 = new byte[self.image_data_size * 2]
				for (i = 0 i < self.image_data_size i += 2)
					BGRA32[i * 2 + 1] = self.image_data[i + 1]# G
					BGRA32[i * 2 + 2] = self.image_data[i]# R
					BGRA32[i * 2 + 3] = 255# A
				self.SetBGRA32Info(BGRA32)

		elif self.m_TextureFormat == TextureFormat.R8: # test pass
				# 转BGRA32
				BGRA32 = new byte[self.image_data_size * 4]
				for i in range(self.image_data_size):
					BGRA32[i * 4 + 2] = self.image_data[i]# R
					BGRA32[i * 4 + 3] = 255# A
				self.SetBGRA32Info(BGRA32)


	def self.SetBGRA32Info(self, BGRA32 : bytes)
		self.image_data = BGRA32
		self.image_data_size = len(BGRA32)
		self.self.dwFlags2 = 0x41
		self.self.dwRGBBitCount = 0x20
		self.self.dwRBitMask = 0xFF0000
		self.self.dwGBitMask = 0xFF00
		self.self.dwBBitMask = 0xFF
		self.self.dwABitMask = -16777216

	def SwapBytesForXbox(self.platform : BuildTarget):
		if self.platform == BuildTarget.XBOX360: # swap bytes for Xbox confirmed, PS3 not encountered
			for _ in range(0,self.image_data_size,2):
				self.image_data[i:i+2] = self.image_data[i:i+2][::-1]

	def GetExtensionName(self):
		TF = self.m_TextureFormat
		if TF in [
			TextureFormat.Alpha8,
			TextureFormat.ARGB4444,
			TextureFormat.RGB24,
			TextureFormat.RGBA32,
			TextureFormat.ARGB32,
			TextureFormat.RGB565,
			TextureFormat.R16,
			TextureFormat.DXT1,
			TextureFormat.DXT5,
			TextureFormat.RGBA4444,
			TextureFormat.BGRA32,
			TextureFormat.RG16,
			TextureFormat.R8,
		]:
				return ".dds"
		elif TF in [
			TextureFormat.DXT1Crunched,
			TextureFormat.DXT5Crunched,
			TextureFormat.ETC_RGB4Crunched,
			TextureFormat.ETC2_RGBA8Crunched,
		]:
				return ".crn"
		elif TF in [
			TextureFormat.YUY2,
			TextureFormat.PVRTC_RGB2,
			TextureFormat.PVRTC_RGBA2,
			TextureFormat.PVRTC_RGB4,
			TextureFormat.PVRTC_RGBA4,
			TextureFormat.ETC_RGB4,
			TextureFormat.ETC2_RGB,
			TextureFormat.ETC2_RGBA1,
			TextureFormat.ETC2_RGBA8,
			TextureFormat.ASTC_RGB_4x4,
			TextureFormat.ASTC_RGB_5x5,
			TextureFormat.ASTC_RGB_6x6,
			TextureFormat.ASTC_RGB_8x8,
			TextureFormat.ASTC_RGB_10x10,
			TextureFormat.ASTC_RGB_12x12,
			TextureFormat.ASTC_RGBA_4x4,
			TextureFormat.ASTC_RGBA_5x5,
			TextureFormat.ASTC_RGBA_6x6,
			TextureFormat.ASTC_RGBA_8x8,
			TextureFormat.ASTC_RGBA_10x10,
			TextureFormat.ASTC_RGBA_12x12,
			TextureFormat.ETC_RGB4_3DS,
			TextureFormat.ETC_RGBA8_3DS,
		]:
				return ".pvr"
		elif TF in [
			TextureFormat.RHalf,
			TextureFormat.RGHalf,
			TextureFormat.RGBAHalf,
			TextureFormat.RFloat,
			TextureFormat.RGFloat,
			TextureFormat.RGBAFloat,
			TextureFormat.BC4,
			TextureFormat.BC5,
			TextureFormat.BC6H,
			TextureFormat.BC7,
			TextureFormat.ATC_RGB4,
			TextureFormat.ATC_RGBA8,
			TextureFormat.EAC_R,
			TextureFormat.EAC_R_SIGNED,
			TextureFormat.EAC_RG,
			TextureFormat.EAC_RG_SIGNED,
		]:
				return ".ktx"
		else:
				return ".tex"


	def ConvertToContainer(self) -> bytes:
		if not self.image_data:
			return b''
		TF = self.m_TextureFormat
		if TF in [
			TextureFormat.Alpha8,
			TextureFormat.ARGB4444,
			TextureFormat.RGB24,
			TextureFormat.RGBA32,
			TextureFormat.ARGB32,
			TextureFormat.RGB565,
			TextureFormat.R16,
			TextureFormat.DXT1,
			TextureFormat.DXT5,
			TextureFormat.RGBA4444,
			TextureFormat.BGRA32,
			TextureFormat.RG16,
			TextureFormat.R8,
		]:
				return self.ConvertToDDS()
		elif TF in [
			TextureFormat.YUY2,
			TextureFormat.PVRTC_RGB2,
			TextureFormat.PVRTC_RGBA2,
			TextureFormat.PVRTC_RGB4,
			TextureFormat.PVRTC_RGBA4,
			TextureFormat.ETC_RGB4,
			TextureFormat.ETC2_RGB,
			TextureFormat.ETC2_RGBA1,
			TextureFormat.ETC2_RGBA8,
			TextureFormat.ASTC_RGB_4x4,
			TextureFormat.ASTC_RGB_5x5,
			TextureFormat.ASTC_RGB_6x6,
			TextureFormat.ASTC_RGB_8x8,
			TextureFormat.ASTC_RGB_10x10,
			TextureFormat.ASTC_RGB_12x12,
			TextureFormat.ASTC_RGBA_4x4,
			TextureFormat.ASTC_RGBA_5x5,
			TextureFormat.ASTC_RGBA_6x6,
			TextureFormat.ASTC_RGBA_8x8,
			TextureFormat.ASTC_RGBA_10x10,
			TextureFormat.ASTC_RGBA_12x12,
			TextureFormat.ETC_RGB4_3DS,
			TextureFormat.ETC_RGBA8_3DS,
		]:
				return self.ConvertToPVR()
		elif TF in [
			TextureFormat.RHalf,
			TextureFormat.RGHalf,
			TextureFormat.RGBAHalf,
			TextureFormat.RFloat,
			TextureFormat.RGFloat,
			TextureFormat.RGBAFloat,
			TextureFormat.BC4,
			TextureFormat.BC5,
			TextureFormat.BC6H,
			TextureFormat.BC7,
			TextureFormat.ATC_RGB4,
			TextureFormat.ATC_RGBA8,
			TextureFormat.EAC_R,
			TextureFormat.EAC_R_SIGNED,
			TextureFormat.EAC_RG,
			TextureFormat.EAC_RG_SIGNED,
			]:
				return self.ConvertToKTX()
		else:
				return self.image_data



			def ConvertToDDS(self) -> bytes:
				return b''.join([
					self.dwMagic,
					int_to_byte(self.self.dwFlags),
					int_to_byte(self.m_Height),
					int_to_byte(self.m_Width),
					int_to_byte(self.dwPitchOrLinearSize),
					int_to_byte(self.self.dwMipMapCount),
					int_to_byte(self.dwSize),
					int_to_byte(self.self.dwFlags2),
					int_to_byte(self.dwFourCC),
					int_to_byte(self.self.dwRGBBitCount),
					int_to_byte(self.self.dwRBitMask),
					int_to_byte(self.self.dwGBitMask),
					int_to_byte(self.self.dwBBitMask),
					int_to_byte(self.dwABitMask),
					int_to_byte(self.self.dwCaps),
					int_to_byte(self.self.dwCaps2),
					self.image_data
				])
			
			def ConvertToPVR(self) -> bytes:
				return b''.join([
					self.pvrself.version,
					int_to_byte(self.pvrFlags),
					int_to_byte(self.self.pvrPixelFormat),
					int_to_byte(self.pvrColourSpace),
					int_to_byte(self.pvrChannelType),
					int_to_byte(self.m_Height),
					int_to_byte(self.m_Width),
					int_to_byte(self.pvrDepth),
					int_to_byte(self.pvrNumSurfaces),
					int_to_byte(self.pvrNumFaces),
					int_to_byte(self.self.dwMipMapCount),
					int_to_byte(self.pvrMetaDataSize),
					self.image_data
				])
			
			def ConvertToKTX(self) -> bytes:
				return b''.join([
					int_to_byte(KTXHeader.IDENTIFIER),
					int_to_byte(KTXHeader.ENDIANESS_LE),
					int_to_byte(self.glType),
					int_to_byte(self.glTypeSize),
					int_to_byte(self.glFormat),
					int_to_byte(self.self.glInternalFormat),
					int_to_byte(self.self.glBaseInternalFormat),
					int_to_byte(self.m_Width),
					int_to_byte(self.m_Height),
					int_to_byte(self.pixelDepth),
					int_to_byte(self.numberOfArrayElements),
					int_to_byte(self.numberOfFaces),
					int_to_byte(self.numberOfMipmapLevels),
					int_to_byte(self.bytesOfKeyValueData),
					int_to_byte(self.image_data_size),
					self.image_data
				])
			
			
			def ConvertToBitmap(self, flip : bool) -> Image:
				if not self.image_data:
					return b''
			
				TF = self.m_TextureFormat
				if TF in [
					TextureFormat.Alpha8,
					TextureFormat.ARGB4444,
					TextureFormat.RGB24,
					TextureFormat.RGBA32,
					TextureFormat.ARGB32,
					TextureFormat.R16,
					TextureFormat.RGBA4444,
					TextureFormat.BGRA32,
					TextureFormat.RG16,
					TextureFormat.R8,
				]:
						bitmap = BGRA32ToBitmap()
				elif TF == TextureFormat.RGB565:
						bitmap = RGB565ToBitmap()
				elif TF in [
					TextureFormat.YUY2,
					TextureFormat.PVRTC_RGB2,
					TextureFormat.PVRTC_RGBA2,
					TextureFormat.PVRTC_RGB4,
					TextureFormat.PVRTC_RGBA4,
					TextureFormat.ETC_RGB4,
					TextureFormat.ETC2_RGB,
					TextureFormat.ETC2_RGBA1,
					TextureFormat.ETC2_RGBA8,
					TextureFormat.ETC_RGB4_3DS,
					TextureFormat.ETC_RGBA8_3DS,
				]:
						bitmap = PVRToBitmap(ConvertToPVR())
				elif TF in [
					TextureFormat.DXT1,
					TextureFormat.DXT5,
					TextureFormat.RHalf,
					TextureFormat.RGHalf,
					TextureFormat.RGBAHalf,
					TextureFormat.RFloat,
					TextureFormat.RGFloat,
					TextureFormat.RGBAFloat,
					TextureFormat.RGB9e5Float,
					TextureFormat.ATC_RGB4,
					TextureFormat.ATC_RGBA8,
					TextureFormat.EAC_R,
					TextureFormat.EAC_R_SIGNED,
					TextureFormat.EAC_RG,
					TextureFormat.EAC_RG_SIGNED,
				]:
						bitmap = TextureConverter()
				elif TF in [
					TextureFormat.BC4,
					TextureFormat.BC5,
					TextureFormat.BC6H,
					TextureFormat.BC7,
				]:
						bitmap = TexgenPackDecode()
				elif TF in [
					TextureFormat.DXT1Crunched,
					TextureFormat.DXT5Crunched,
				]:
						DecompressCRN()
						bitmap = TextureConverter()
				elif TF in [
					TextureFormat.ETC_RGB4Crunched,
					TextureFormat.ETC2_RGBA8Crunched,
				]:
						DecompressCRN()
						bitmap = PVRToBitmap(ConvertToPVR())
				elif TF in [
					TextureFormat.ASTC_RGB_4x4,
					TextureFormat.ASTC_RGB_5x5,
					TextureFormat.ASTC_RGB_6x6,
					TextureFormat.ASTC_RGB_8x8,
					TextureFormat.ASTC_RGB_10x10,
					TextureFormat.ASTC_RGB_12x12,
					TextureFormat.ASTC_RGBA_4x4,
					TextureFormat.ASTC_RGBA_5x5,
					TextureFormat.ASTC_RGBA_6x6,
					TextureFormat.ASTC_RGBA_8x8,
					TextureFormat.ASTC_RGBA_10x10,
					TextureFormat.ASTC_RGBA_12x12,
				]:
						bitmap = DecodeASTC()
				else:
					return b''
			
				if bitmap and flip:
					bitmap = ImageOps.flip(bitmap)
				return bitmap


class KTXHeader:
	IDENTIFIER = bytearray([ 0xAB, 0x4B, 0x54, 0x58, 0x20, 0x31, 0x31, 0xBB, 0x0D, 0x0A, 0x1A, 0x0A])
	ENDIANESS_LE = bytearray([ 1, 2, 3, 4] )
	#  constants for self.glInternalFormat
	GL_ETC1_RGB8_OES = 0x8D64

	GL_COMPRESSED_RGB_PVRTC_4BPPV1_IMG = 0x8C00
	GL_COMPRESSED_RGB_PVRTC_2BPPV1_IMG = 0x8C01
	GL_COMPRESSED_RGBA_PVRTC_4BPPV1_IMG = 0x8C02
	GL_COMPRESSED_RGBA_PVRTC_2BPPV1_IMG = 0x8C03

	GL_ATC_RGB_AMD = 0x8C92
	GL_ATC_RGBA_INTERPOLATED_ALPHA_AMD = 0x87EE

	GL_COMPRESSED_RGB8_ETC2 = 0x9274
	GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2 = 0x9276
	GL_COMPRESSED_RGBA8_ETC2_EAC = 0x9278
	GL_COMPRESSED_R11_EAC = 0x9270
	GL_COMPRESSED_SIGNED_R11_EAC = 0x9271
	GL_COMPRESSED_RG11_EAC = 0x9272
	GL_COMPRESSED_SIGNED_RG11_EAC = 0x9273

	GL_COMPRESSED_RED_RGTC1 = 0x8DBB
	GL_COMPRESSED_RG_RGTC2 = 0x8DBD
	GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT = 0x8E8F
	GL_COMPRESSED_RGBA_BPTC_UNORM = 0x8E8C

	GL_R16F = 0x822D
	GL_RG16F = 0x822F
	GL_RGBA16F = 0x881A
	GL_R32F = 0x822E
	GL_RG32F = 0x8230
	GL_RGBA32F = 0x8814

	#  constants for self.glBaseInternalFormat
	GL_RED = 0x1903
	GL_RGB = 0x1907
	GL_RGBA = 0x1908
	GL_RG = 0x8227

# from TextureConverter.h
class QFORMAT(IntEnum):
	#  General formats
	self.q_format_RGBA_8UI = 1,
	self.q_format_RGBA_8I,
	self.q_format_RGB5_A1UI,
	self.q_format_RGBA_4444,
	self.q_format_RGBA_16UI,
	self.q_format_RGBA_16I,
	self.q_format_RGBA_32UI,
	self.q_format_RGBA_32I,

	self.q_format_PALETTE_8_RGBA_8888,
	self.q_format_PALETTE_8_RGBA_5551,
	self.q_format_PALETTE_8_RGBA_4444,
	self.q_format_PALETTE_4_RGBA_8888,
	self.q_format_PALETTE_4_RGBA_5551,
	self.q_format_PALETTE_4_RGBA_4444,
	self.q_format_PALETTE_1_RGBA_8888,
	self.q_format_PALETTE_8_RGB_888,
	self.q_format_PALETTE_8_RGB_565,
	self.q_format_PALETTE_4_RGB_888,
	self.q_format_PALETTE_4_RGB_565,

	self.q_format_R2_GBA10UI,
	self.q_format_RGB10_A2UI,
	self.q_format_RGB10_A2I,
	self.q_format_RGBA_F,
	self.q_format_RGBA_HF,

	self.q_format_RGB9_E5,   #  Last five bits are exponent bits (Read following section in GLES3 spec: "3.8.17 Shared Exponent Texture Color Conself.version")
	self.q_format_RGB_8UI,
	self.q_format_RGB_8I,
	self.q_format_RGB_565,
	self.q_format_RGB_16UI,
	self.q_format_RGB_16I,
	self.q_format_RGB_32UI,
	self.q_format_RGB_32I,

	self.q_format_RGB_F,
	self.q_format_RGB_HF,
	self.q_format_RGB_11_11_10_F,

	self.q_format_RG_F,
	self.q_format_RG_HF,
	self.q_format_RG_32UI,
	self.q_format_RG_32I,
	self.q_format_RG_16I,
	self.q_format_RG_16UI,
	self.q_format_RG_8I,
	self.q_format_RG_8UI,
	self.q_format_RG_S88,

	self.q_format_R_32UI,
	self.q_format_R_32I,
	self.q_format_R_F,
	self.q_format_R_16F,
	self.q_format_R_16I,
	self.q_format_R_16UI,
	self.q_format_R_8I,
	self.q_format_R_8UI,

	self.q_format_LUMINANCE_ALPHA_88,
	self.q_format_LUMINANCE_8,
	self.q_format_ALPHA_8,

	self.q_format_LUMINANCE_ALPHA_F,
	self.q_format_LUMINANCE_F,
	self.q_format_ALPHA_F,
	self.q_format_LUMINANCE_ALPHA_HF,
	self.q_format_LUMINANCE_HF,
	self.q_format_ALPHA_HF,
	self.q_format_DEPTH_16,
	self.q_format_DEPTH_24,
	self.q_format_DEPTH_24_STENCIL_8,
	self.q_format_DEPTH_32,

	self.q_format_BGR_565,
	self.q_format_BGRA_8888,
	self.q_format_BGRA_5551,
	self.q_format_BGRX_8888,
	self.q_format_BGRA_4444,
	#  Compressed formats
	self.q_format_ATITC_RGBA,
	self.q_format_ATC_RGBA_EXPLICIT_ALPHA = self.q_format_ATITC_RGBA,
	self.q_format_ATITC_RGB,
	self.q_format_ATC_RGB = self.q_format_ATITC_RGB,
	self.q_format_ATC_RGBA_INTERPOLATED_ALPHA,
	self.q_format_ETC1_RGB8,
	self.q_format_3DC_X,
	self.q_format_3DC_XY,

	self.q_format_ETC2_RGB8,
	self.q_format_ETC2_RGBA8,
	self.q_format_ETC2_RGB8_PUNCHTHROUGH_ALPHA1,
	self.q_format_ETC2_SRGB8,
	self.q_format_ETC2_SRGB8_ALPHA8,
	self.q_format_ETC2_SRGB8_PUNCHTHROUGH_ALPHA1,
	self.q_format_EAC_R_SIGNED,
	self.q_format_EAC_R_UNSIGNED,
	self.q_format_EAC_RG_SIGNED,
	self.q_format_EAC_RG_UNSIGNED,

	self.q_format_S3TC_DXT1_RGB,
	self.q_format_S3TC_DXT1_RGBA,
	self.q_format_S3TC_DXT3_RGBA,
	self.q_format_S3TC_DXT5_RGBA,

	#  YUV formats
	self.q_format_AYUV_32,
	self.q_format_I444_24,
	self.q_format_YUYV_16,
	self.q_format_UYVY_16,
	self.q_format_I420_12,
	self.q_format_YV12_12,
	self.q_format_NV21_12,
	self.q_format_NV12_12,

	#  ASTC Format
	self.q_format_ASTC_8,
	self.q_format_ASTC_16,

class texgenpack_self.texturetype(IntEnum):
	RGTC1 = 0,
	RGTC2 = 1,
	BPTC_FLOAT = 2,
	BPTC = 3



########################################################################################
# PVR parser
# https://github.com/GreyRook/python-pvr
import sys
from bitstring import ConstBitStream


def scale_to_255(color, size):
    number = float(color) / 2**size
    return int(number * 255)


def compact(x):
    x &= 0x55555555                  # x = -f-e -d-c -b-a -9-8 -7-6 -5-4 -3-2 -1-0
    x = (x ^ (x >> 1)) & 0x33333333  # x = --fe --dc --ba --98 --76 --54 --32 --10
    x = (x ^ (x >> 2)) & 0x0f0f0f0f  # x = ---- fedc ---- ba98 ---- 7654 ---- 3210
    x = (x ^ (x >> 4)) & 0x00ff00ff  # x = ---- ---- fedc ba98 ---- ---- 7654 3210
    x = (x ^ (x >> 8)) & 0x0000ffff
    return x


def decode_morton(i):
    x = compact(i)
    y = compact(i >> 1)
    return x, y


class PVRImage(object):
    def __init__(self):
        self.img_a = None
        self.img_b = None
        self.img_mod = None

    @classmethod
    def from_file(cls, file_path):
        re = cls()

        with open(file_path, 'rb') as f:
            bit_stream = ConstBitStream(f)
            version = bit_stream.read('hex:32')
            flags = bit_stream.read('uintle:32')
            pixel_format = bit_stream.read('uintle:64')
            colour_space = bit_stream.read('uintle:32')
            channel_type = bit_stream.read('uintle:32')
            height = bit_stream.read('uintle:32')
            width = bit_stream.read('uintle:32')
            depth = bit_stream.read('uintle:32')
            num_surfaces = bit_stream.read('uintle:32')
            num_faces = bit_stream.read('uintle:32')
            mip_map_count = bit_stream.read('uintle:32')
            meta_data_size = bit_stream.read('uintle:32')
            meta_data = bit_stream.read('bytes:{}'.format(meta_data_size))

            # for now not supported:
            # * mip map
            # * multiples surfaces
            # * multiple faces
            assert mip_map_count == 1
            assert num_surfaces == 1
            assert num_faces == 1

            for mip in xrange(mip_map_count):
                for surface in xrange(num_surfaces):
                    for face in xrange(num_faces):
                        for slice in xrange(depth):
                            image_width = width/4/2**(mip)
                            image_height = height/4/2**(mip)

                            img_a = PIL.Image.new('RGBA', (width/4, height/4))
                            img_a_data = img_a.load()
                            img_b = PIL.Image.new('RGBA', (width/4, height/4))
                            img_b_data = img_b.load()
                            img_mod = PIL.Image.new('RGBA', (width, height))
                            img_mod_data = img_mod.load()

                            for i in xrange(image_width * image_height):
                                    pixel, row = decode_morton(i)
                                    modulation_data = bit_stream.read('bits:32')
                                    byte0 = bit_stream.read('bits:8')
                                    byte1 = bit_stream.read('bits:8')
                                    byte2 = bit_stream.read('bits:8')
                                    byte3 = bit_stream.read('bits:8')

                                    color_mode = byte3.read('bool')

                                    r = g = b = a = 255
                                    if color_mode:
                                        r = byte3.read('uint:5')
                                        g = (byte3.read('bits:2') + byte2.read('bits:3')).read('uint:5')
                                        b = byte2.read('uint:5')
                                        r = scale_to_255(r, 5)
                                        g = scale_to_255(g, 5)
                                        b = scale_to_255(b, 5)
                                    else:
                                        a = byte3.read('uint:3')
                                        r = byte3.read('uint:4')
                                        g = byte2.read('uint:4')
                                        b = byte2.read('uint:4')
                                        a = scale_to_255(a, 3)
                                        r = scale_to_255(r, 4)
                                        g = scale_to_255(g, 4)
                                        b = scale_to_255(b, 4)
                                    img_b_data[row, pixel] = (r, g, b, a)

                                    color_mode = byte1.read('bool')


                                    r = g = b = a = 255
                                    if color_mode:
                                        r = byte1.read('uint:5')
                                        g = (byte1.read('bits:2') + byte0.read('bits:3')).read('uint:5')
                                        b = byte0.read('uint:4')
                                        r = scale_to_255(r, 5)
                                        g = scale_to_255(g, 5)
                                        b = scale_to_255(b, 4)
                                    else:
                                        a = byte1.read('uint:3')
                                        r = byte1.read('uint:4')
                                        g = byte0.read('uint:4')
                                        b = byte0.read('uint:3')
                                        a = scale_to_255(a, 3)
                                        r = scale_to_255(r, 4)
                                        g = scale_to_255(g, 4)
                                        b = scale_to_255(b, 3)

                                    img_a_data[row, pixel] = (r, g, b, a)

                                    mode = byte0.read('bool')

                                    for r in xrange(4):
                                        for c in xrange(4):
                                            first = modulation_data.read('uint:1')
                                            last = modulation_data.read('uint:1')
                                            value = 0
                                            if first == 0 and last == 0:
                                                value = 0
                                            elif first == 0 and last == 1:
                                                value = 3
                                            elif first == 1 and last == 0:
                                                value = 5
                                            elif first == 1 and last == 1:
                                                value = 8
                                            texel_row = 3 - r + row*4
                                            texel_col = 3 - c + pixel*4
                                            img_mod_data[texel_row, texel_col] = (0, 0, 0, int(float(value)/8*255))

                            re.img_a = img_a
                            re.img_b = img_b
                            re.img_mod = img_mod # .save('img_mod_{}.png'.format(mip))
                            return re