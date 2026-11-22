package com.alvsia.ai.uncensored

import android.content.ContentResolver
import android.net.Uri
import java.io.BufferedInputStream
import java.security.MessageDigest

enum class SmartOperation { ANALYZE, LUA_DETECT, LUA_DECOMPILE, LUA_RECONSTRUCT, PAK_DETECT, PAK_INDEX, PAK_EXTRACT, PAK_REPACK, BATCH_AUDIT }
data class SmartCapability(val operation: SmartOperation, val available: Boolean, val reason: String)
data class SmartPipelineReport(val fileName:String,val size:Long,val sha256:String,val type:String,val capabilities:List<SmartCapability>,val diagnostics:List<String>)

object SmartPipeline {
    private const val BUFFER = 1024 * 1024
    fun run(resolver:ContentResolver, uri:Uri):SmartPipelineReport {
        val name=resolver.query(uri,arrayOf(android.provider.OpenableColumns.DISPLAY_NAME),null,null,null)?.use{c->if(c.moveToFirst())c.getString(0)else"input"}?:"input"
        val size=resolver.query(uri,arrayOf(android.provider.OpenableColumns.SIZE),null,null,null)?.use{c->if(c.moveToFirst()&&!c.isNull(0))c.getLong(0)else-1L}?:-1L
        val digest=MessageDigest.getInstance("SHA-256"); val head=ByteArray(128*1024); var headLen=0
        resolver.openInputStream(uri).use{raw->
            requireNotNull(raw){"Tidak dapat membuka input."}
            BufferedInputStream(raw,BUFFER).use{input->
                val buffer=ByteArray(BUFFER)
                while(true){val n=input.read(buffer);if(n<0)break;digest.update(buffer,0,n);if(headLen<head.size){val take=minOf(n,head.size-headLen);System.arraycopy(buffer,0,head,headLen,take);headLen+=take}}
            }
        }
        val h=head.copyOf(headLen);val type=SmartFormat.detect(name,h)
        val diagnostics=when(type){"LUA"->LuaBinaryInspector.inspect(h).diagnostics;"UE4_PAK"->listOf("UE4 PAK magic terdeteksi.","Index parser/encryption adapter harus memilih format/version sebelum membaca index.","File asli tetap read-only sampai operasi eksplisit REPACK.");else->listOf("Format: "+type,"Streaming SHA-256 selesai.")}
        return SmartPipelineReport(name,size,digest.digest().joinToString(""){"%02x".format(it.toInt()and 255)},type,capabilities(type),diagnostics)
    }
    private fun capabilities(type:String)=when(type){
        "LUA"->listOf(SmartCapability(SmartOperation.LUA_DETECT,true,"Header/source detection"),SmartCapability(SmartOperation.LUA_DECOMPILE,false,"Decompiler adapter belum dibundel"),SmartCapability(SmartOperation.LUA_RECONSTRUCT,false,"Reconstruction adapter belum dibundel"),SmartCapability(SmartOperation.BATCH_AUDIT,true,"Streaming audit"))
        "UE4_PAK"->listOf(SmartCapability(SmartOperation.PAK_DETECT,true,"Magic/version probe"),SmartCapability(SmartOperation.PAK_INDEX,false,"UE4/Tencent index adapter belum dibundel"),SmartCapability(SmartOperation.PAK_EXTRACT,false,"Memerlukan index + compression/encryption adapter"),SmartCapability(SmartOperation.PAK_REPACK,false,"Memerlukan lossless index writer"))
        else->listOf(SmartCapability(SmartOperation.ANALYZE,true,"Generic streaming analyzer"))
    }
}
object SmartFormat{
    fun detect(name:String,b:ByteArray):String{
        val n=name.lowercase()
        if(b.size>=4&&b.copyOfRange(0,4).contentEquals(byteArrayOf(0x5A,0x6F,0x12.toByte(),0xE1.toByte())))return"UE4_PAK"
        if(b.size>=4&&b.copyOfRange(0,4).contentEquals(byteArrayOf(0x1B,0x4C,0x75,0x61)))return"LUA"
        if(n.endsWith(".lua")||n.endsWith(".luac")||n.endsWith(".lua.enc"))return"LUA"
        if(b.size>=4&&b[0]==0x50.toByte()&&b[1]==0x4B.toByte())return"ZIP_CONTAINER"
        if(b.size>=4&&b[0]==0x7F.toByte()&&b[1]=='E'.code.toByte()&&b[2]=='L'.code.toByte()&&b[3]=='F'.code.toByte())return"ELF"
        if(b.size>=2&&b[0]=='M'.code.toByte()&&b[1]=='Z'.code.toByte())return"PE"
        if(b.size>=4&&b[0]=='d'.code.toByte()&&b[1]=='e'.code.toByte()&&b[2]=='x'.code.toByte()&&b[3]==0x0A.toByte())return"DEX"
        return"BINARY"
    }
}
object LuaBinaryInspector{
    data class Result(val validHeader:Boolean,val version:String,val format:Int?,val diagnostics:List<String>)
    fun inspect(b:ByteArray):Result{
        if(b.size<6)return Result(false,"unknown",null,listOf("Input terlalu pendek untuk header Lua."))
        if(!(b[0]==0x1B.toByte()&&b[1]=='L'.code.toByte()&&b[2]=='u'.code.toByte()&&b[3]=='a'.code.toByte()))return Result(false,"unknown",null,listOf("Magic Lua tidak ditemukan pada offset 0."))
        val versionByte=b[4].toInt()and 255;val version="0x%02X".format(versionByte);val format=b[5].toInt()and 255
        val d=mutableListOf("Lua magic valid.","Version="+version,"Format="+format)
        when(versionByte){0x51,0x52,0x53,0x54->d+="Versi Lua 5.x family terdeteksi.";else->d+="Versi tidak dikenal; jangan dipaksa ke parser 5.3."}
        if(versionByte==0x53&&b.size>=18){val endian=if((b[6].toInt()and 255)==1)"little"else"non-little";d+="Lua 5.3 candidate: endianness="+endian+"."}
        return Result(true,version,format,d)
    }
}
