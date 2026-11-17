package com.alvsia.ai.uncensored

data class AiModel(
    val id: String,
    val name: String,
    val provider: String,
    val family: String,
    val tags: List<String>,
    val sourceUrl: String,
    val licenseUrl: String,
    val remote: Boolean = true
)

object ModelCatalog {
    val starter = listOf(
        AiModel("openai/gpt-oss-20b","GPT-OSS 20B (Groq)","Groq","GPT-OSS",listOf("fast","coding"),"https://groq.com","https://groq.com"),
        AiModel("qwen3.5-27b-heretic","Qwen 3.5 27B Heretic","Hugging Face","Qwen",listOf("reasoning","coding","uncensored"),"https://huggingface.co","https://huggingface.co"),
        AiModel("qwen3.6-27b-uncensored-heretic","Qwen 3.6 27B Uncensored Heretic","Hugging Face","Qwen",listOf("reasoning","coding","uncensored"),"https://huggingface.co","https://huggingface.co"),
        AiModel("glm-4.7-flash-absolute-heresy","GLM 4.7 Flash Absolute Heresy","Hugging Face","GLM",listOf("reasoning","fast","uncensored"),"https://huggingface.co","https://huggingface.co"),
        AiModel("deepseek-r1","DeepSeek R1","Ollama","DeepSeek",listOf("reasoning","research"),"https://ollama.com","https://ollama.com"),
        AiModel("gpt-oss-120b","GPT-OSS 120B","Ollama","GPT-OSS",listOf("reasoning","coding"),"https://ollama.com","https://ollama.com"),
        AiModel("gpt-oss-20b","GPT-OSS 20B","Ollama","GPT-OSS",listOf("fast","coding"),"https://ollama.com","https://ollama.com"),
        AiModel("gemma-4-12b-heretic","Gemma 4 12B Heretic","Hugging Face","Gemma",listOf("general","uncensored"),"https://huggingface.co","https://huggingface.co"),
        AiModel("qwen3-vl-8b-abliterated","Qwen3-VL 8B Abliterated","Hugging Face","Qwen",listOf("vision","coding","uncensored"),"https://huggingface.co","https://huggingface.co"),
        AiModel("hermes-3-llama-3.1-8b","Hermes 3 Llama 3.1 8B","Hugging Face","Llama",listOf("fast","agent"),"https://huggingface.co","https://huggingface.co"),
        AiModel("llama-3.1-8b-abliterated","Llama 3.1 8B Abliterated","Hugging Face","Llama",listOf("fast","uncensored"),"https://huggingface.co","https://huggingface.co"),
        AiModel("qwen3.6-35b-moe-abliterated","Qwen 3.6 35B MoE Abliterated","Hugging Face","Qwen",listOf("reasoning","coding","uncensored"),"https://huggingface.co","https://huggingface.co"),
        AiModel("mistral-small-3","Mistral Small 3","Ollama","Mistral",listOf("coding","fast"),"https://ollama.com","https://ollama.com"),
        AiModel("phi-4","Phi 4","Ollama","Phi",listOf("fast","coding"),"https://ollama.com","https://ollama.com"),
        AiModel("llama-4","Llama 4","Ollama","Llama",listOf("general","vision"),"https://ollama.com","https://ollama.com"),
        AiModel("gemma-4","Gemma 4","Ollama","Gemma",listOf("general","coding"),"https://ollama.com","https://ollama.com"),
        AiModel("glm-4.7-flash","GLM 4.7 Flash","Ollama","GLM",listOf("fast","coding"),"https://ollama.com","https://ollama.com"),
        AiModel("qwen-coder","Qwen Coder","Ollama","Qwen",listOf("coding","agent"),"https://ollama.com","https://ollama.com"),
        AiModel("deepseek-coder","DeepSeek Coder","Ollama","DeepSeek",listOf("coding","agent"),"https://ollama.com","https://ollama.com")
    )
}
