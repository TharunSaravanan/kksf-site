package com.adhigopal.thirukkural

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

// Mirrors apps/build_app_data.py output (assets/thirukkural_data.json).

data class Tradition(val key: String, val label: String)
data class Chapter(val n: Int, val ta: String, val tr: String, val en: String, val paal: String, val start: Int, val end: Int)
data class Paal(val key: String, val en: String, val ta: String, val sub: String)
data class CrossRef(val q: String, val isQuote: Boolean, val ex: String, val tb: String, val s: String, val c: String)
data class RealLifeExample(
    val title: String, val date: String, val place: String,
    val event: String, val ex: String, val tb: String, val c: List<String>,
)
data class Kural(
    val n: Int, val ta: String, val tr: String, val meaning: String,
    val elementary: String, val university: String, val src: List<String>,
    val x: Map<String, CrossRef>, val rle: RealLifeExample?,
) {
    val chapterNumber: Int get() = (n - 1) / 10 + 1
}
data class Source(val title: String, val by: String, val publisher: String, val url: String, val tier: String)

class AppData(
    val traditions: List<Tradition>,
    val hasRealLifeExample: Boolean,
    val chapters: List<Chapter>,
    val paals: List<Paal>,
    val kurals: List<Kural>,
    val sources: Map<String, Source>,
    val pageHome: String,
    val pageLearnMore: String,
    val pageHistoricalTexts: String,
) {
    val kuralByNumber: Map<Int, Kural> = kurals.associateBy { it.n }
    val chapterByNumber: Map<Int, Chapter> = chapters.associateBy { it.n }

    fun kuralsIn(ch: Chapter): List<Kural> = (ch.start..ch.end).mapNotNull { kuralByNumber[it] }
    fun chaptersIn(paal: String): List<Chapter> = chapters.filter { it.paal == paal }

    fun search(query: String): List<Kural> {
        val q = query.trim().lowercase()
        if (q.isEmpty()) return emptyList()
        q.toIntOrNull()?.let { n -> kuralByNumber[n]?.let { return listOf(it) } }
        return kurals.filter { k ->
            val ch = chapterByNumber[k.chapterNumber]
            k.ta.lowercase().contains(q) || k.tr.lowercase().contains(q) || k.meaning.lowercase().contains(q) ||
                (ch != null && (ch.en.lowercase().contains(q) || ch.ta.contains(q) || ch.tr.lowercase().contains(q)))
        }
    }

    /** Page-local numbered citations: base Tamil-text sources first, then every source used, in reading order. */
    fun citationIndex(k: Kural): LinkedHashMap<String, Int> {
        val order = LinkedHashMap<String, Int>()
        fun add(c: String) { if (c.isNotEmpty() && c !in order) order[c] = order.size + 1 }
        k.src.forEach(::add)
        traditions.forEach { t -> k.x[t.key]?.let { add(it.c) } }
        if (hasRealLifeExample) k.rle?.c?.forEach(::add)
        return order
    }

    companion object {
        @Volatile private var cached: AppData? = null

        fun load(context: Context): AppData = cached ?: synchronized(this) {
            cached ?: parse(context.assets.open("thirukkural_data.json").bufferedReader(Charsets.UTF_8).use { it.readText() })
                .also { cached = it }
        }

        private fun JSONArray.objects(): List<JSONObject> = (0 until length()).map { getJSONObject(it) }
        private fun JSONArray.strings(): List<String> = (0 until length()).map { getString(it) }

        private fun parse(text: String): AppData {
            val root = JSONObject(text)
            val traditions = root.getJSONArray("traditions").objects().map { Tradition(it.getString("key"), it.getString("label")) }
            val chapters = root.getJSONArray("chapters").objects().map {
                Chapter(it.getInt("n"), it.getString("ta"), it.getString("tr"), it.getString("en"),
                    it.getString("paal"), it.getInt("start"), it.getInt("end"))
            }
            val paals = root.getJSONArray("paals").objects().map {
                Paal(it.getString("key"), it.getString("en"), it.getString("ta"), it.getString("sub"))
            }
            val kurals = root.getJSONArray("kurals").objects().map { o ->
                val xo = o.getJSONObject("x")
                val x = xo.keys().asSequence().associateWith { key ->
                    val c = xo.getJSONObject(key)
                    CrossRef(c.getString("q"), c.getBoolean("isq"), c.getString("ex"), c.getString("tb"),
                        c.getString("s"), c.optString("c", ""))
                }
                val rle = o.optJSONObject("rle")?.let { r ->
                    RealLifeExample(r.getString("title"), r.optString("date"), r.optString("place"),
                        r.getString("event"), r.getString("ex"), r.getString("tb"), r.getJSONArray("c").strings())
                }
                Kural(o.getInt("n"), o.getString("ta"), o.getString("tr"), o.getString("meaning"),
                    o.getString("elementary"), o.getString("university"), o.getJSONArray("src").strings(), x, rle)
            }
            val so = root.getJSONObject("sources")
            val sources = so.keys().asSequence().associateWith { id ->
                val s = so.getJSONObject(id)
                Source(s.optString("title", id), s.optString("by"), s.optString("publisher"), s.optString("url"), s.optString("tier"))
            }
            val pages = root.getJSONObject("pages")
            return AppData(traditions, root.getBoolean("has_real_life_example"), chapters, paals, kurals, sources,
                pages.getString("home"), pages.getString("learn_more"), pages.getString("historical_texts"))
        }
    }
}
