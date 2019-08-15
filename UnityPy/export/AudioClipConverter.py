from ..classes.AudioClip import AudioType, AudioCompressionFormat
import pyfmodex

def FMODSupport(m_AudioClip):
    if m_AudioClip.version[0] < 5:
        if m_AudioClip.m_type in [
                AudioType.AIFF,
                AudioType.IT,
                AudioType.MOD,
                AudioType.S3M,
                AudioType.XM,
                AudioType.XMA,
                AudioType.VAG,
                AudioType.AUDIOQUEUE,
                ]:
            return True
        else:
           return False
    else:
        if m_AudioClip.m_CompressionFormat in [
                AudioCompressionFormat.PCM,
                AudioCompressionFormat.Vorbis,
                AudioCompressionFormat.ADPCM,
                AudioCompressionFormat.MP3,
                AudioCompressionFormat.VAG,
                AudioCompressionFormat.HEVAG,
                AudioCompressionFormat.XMA,
                AudioCompressionFormat.GCADPCM,
                AudioCompressionFormat.ATRAC9,
                ]:
            return True
        else:
            return False

def ConvertToWav(m_AudioClip) -> bytes:
    m_AudioData = m_AudioClip.m_AudioData.Value
    if not m_AudioData:
        return None
    exinfo = FMOD.CREATESOUNDEXINFO()
    result = FMOD.Factory.System_Create(out system)
    if result != FMOD.RESULT.OK:
        return None
    result = system.init(1, FMOD.INITFLAGS.NORMAL, IntPtr.Zero)
    if result != FMOD.RESULT.OK:
        return None
    exinfo.cbsize = Marshal.SizeOf(exinfo)
    exinfo.length = (uint)m_AudioClip.m_Size
    result = system.createSound(m_AudioData, FMOD.MODE.OPENMEMORY, ref exinfo, out sound)
    if result != FMOD.RESULT.OK:
        return None
    result = sound.getSubSound(0, out subsound)
    if result != FMOD.RESULT.OK:
        return None
    result = subsound.getFormat(out type, out format, out int channels, out int bits)
    if result != FMOD.RESULT.OK:
        return None
    result = subsound.getDefaults(out frequency, out int priority)
    if result != FMOD.RESULT.OK:
        return None
    sampleRate = (int)frequency
    result = subsound.getLength(out length, FMOD.TIMEUNIT.PCMBYTES)
    if result != FMOD.RESULT.OK:
        return None
    result = subsound.@lock(0, length, out ptr1, out ptr2, out len1, out len2)
    if result != FMOD.RESULT.OK:
        return None
    byte[] buffer = byte[len1 + 44]
    //添加wav头
    Encoding.UTF8.GetBytes("RIFF").CopyTo(buffer, 0)
    BitConverter.GetBytes(len1 + 36).CopyTo(buffer, 4)
    Encoding.UTF8.GetBytes("WAVEfmt ").CopyTo(buffer, 8)
    BitConverter.GetBytes(16).CopyTo(buffer, 16)
    BitConverter.GetBytes((short)1).CopyTo(buffer, 20)
    BitConverter.GetBytes((short)channels).CopyTo(buffer, 22)
    BitConverter.GetBytes(sampleRate).CopyTo(buffer, 24)
    BitConverter.GetBytes(sampleRate * channels * bits / 8).CopyTo(buffer, 28)
    BitConverter.GetBytes((short)(channels * bits / 8)).CopyTo(buffer, 32)
    BitConverter.GetBytes((short)bits).CopyTo(buffer, 34)
    Encoding.UTF8.GetBytes("data").CopyTo(buffer, 36)
    BitConverter.GetBytes(len1).CopyTo(buffer, 40)
    Marshal.Copy(ptr1, buffer, 44, (int)len1)
    result = subsound.unlock(ptr1, ptr2, len1, len2)
    if result != FMOD.RESULT.OK:
        return None
    subsound.release()
    sound.release()
    system.release()
    return buffer
}

