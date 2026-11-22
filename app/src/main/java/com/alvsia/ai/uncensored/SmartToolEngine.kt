package com.alvsia.ai.uncensored

import android.content.ContentResolver
import android.content.Context
import android.net.Uri
import java.io.BufferedInputStream
import java.io.File
import java.io.FileOutputStream
import java.security.MessageDigest
import java.util.zip.ZipInputStream
import org.json.JSONObject

data class SmartFileReport(val name:String,val type:String,val size:Long,val sha256:String,val detail:String,val warnings:List<String> = emptyList())
data class LuaReport(val kind:String,val version:String,val header:String,val xorCandidates:List<String>,val detail:String)

object SmartToolEngine {
    private const val BUF=1024*1024

    fun materialize(context:Context,uri:Uri):File {
        val name=queryName(context.contentResolver,uri).replace(Regex("[^A-Za-z0-9._-]"),"_")
        val dir=File(context.cacheDir,"smart_inputs").apply{mkdirs()}
        val out=File(dir,"${System.currentTimeMillis()}_$name")
        context.contentResolver.openInputStream(uri).use{raw->requireNotNull(raw);FileOutputStream(out).use{dst->raw.copyTo(dst,BUF)}}
        return out
    }

    fun analyze(context:Context,uri:Uri):SmartFileReport {
        val name=queryName(context.contentResolver,uri); val size=querySize(context.contentResolver,uri)
        val local=materialize(context,uri)
        return try {
            val r=SmartPythonEngine.run(context,local,"analyze")
            SmartFileReport(name,r.optString("type","BINARY"),size,r.optString("sha256",""),r.optString("detail",r.optString("type","Analyzed")))
        } finally { local.delete() }
    }

    fun runOperation(context:Context,uri:Uri,operation:String,output:File?=null):JSONObject {
        val input=materialize(context,uri)
        return try { SmartPythonEngine.run(context,input,operation,output) } finally { input.delete() }
    }

    fun runLuaCustomInject(context:Context, luaUri:Uri, pakUri:Uri, output:File?=null):JSONObject {
        val luaInput=materialize(context,luaUri)
        val pakInput=materialize(context,pakUri)
        return try {
            SmartPythonEngine.run(context,luaInput,"lua_custom_inject",output,mapOf("target_pak" to pakInput.absolutePath))
        } finally {
            luaInput.delete(); pakInput.delete()
        }
    }

    fun inspectLua(bytes:ByteArray):LuaReport {
        if(bytes.size>=4&&bytes.copyOfRange(0,4).contentEquals(byteArrayOf(0x1B,0x4C,0x75,0x61))){
            val v=if(bytes.size>4)"0x%02X".format(bytes[4]) else "unknown"
            val fmt=if(bytes.size>5)"format=0x%02X".format(bytes[5]) else "format=?"
            return LuaReport("Lua bytecode",v,bytes.take(8).toByteArray().toHex()+" "+fmt,emptyList(),"Header Lua valid.")
        }
        val text=bytes.toString(Charsets.UTF_8)
        if(looksLikeLuaSource(text)) return LuaReport("Lua source","text",bytes.take(32).toByteArray().toHex(),emptyList(),"Source Lua terdeteksi.")
        return LuaReport("encrypted/obfuscated candidate","unknown",bytes.take(16).toByteArray().toHex(),emptyList(),"Kirim ke Smart Python Lua pipeline untuk normalisasi/decompile.")
    }

    fun extractZip(context:Context,uri:Uri,outDir:File):Int {
        outDir.mkdirs(); var count=0
        context.contentResolver.openInputStream(uri).use{raw->requireNotNull(raw);ZipInputStream(BufferedInputStream(raw,BUF)).use{zin->
            val buffer=ByteArray(BUF)
            while(true){val e=zin.nextEntry?:break;val target=safeResolve(outDir,e.name);if(e.isDirectory)target.mkdirs()else{target.parentFile?.mkdirs();FileOutputStream(target).use{out->while(true){val n=zin.read(buffer);if(n<0)break;out.write(buffer,0,n)}};count++};zin.closeEntry()}
        }}
        return count
    }

    fun batchClassify(context:Context,uri:Uri):String {
        val input=materialize(context,uri)
        return try { SmartPythonEngine.run(context,input,"analyze").toString(2) } finally { input.delete() }
    }

    private fun queryName(r:ContentResolver,u:Uri):String=r.query(u,arrayOf(android.provider.OpenableColumns.DISPLAY_NAME),null,null,null)?.use{if(it.moveToFirst())it.getString(0)else u.lastPathSegment?:"input"}?:(u.lastPathSegment?:"input")
    private fun querySize(r:ContentResolver,u:Uri):Long=r.query(u,arrayOf(android.provider.OpenableColumns.SIZE),null,null,null)?.use{if(it.moveToFirst()&&!it.isNull(0))it.getLong(0)else-1L}?:-1L
    private fun looksLikeLuaSource(s:String):Boolean{val t=s.trimStart();if(t.startsWith("--")||t.startsWith("local ")||t.startsWith("function ")||t.startsWith("return "))return true;return listOf("function","local","end","then","return").count{s.contains(it)}>=2&&s.count{it=='\u0000'}<3}
    private fun safeResolve(root:File,entry:String):File{val base=root.canonicalFile;val target=File(base,entry).canonicalFile;require(target.path==base.path||target.path.startsWith(base.path+File.separator)){"ZIP entry ditolak: $entry"};return target}
    private fun ByteArray.toHex():String=joinToString(""){"%02x".format(it.toInt()and 255)}
}
