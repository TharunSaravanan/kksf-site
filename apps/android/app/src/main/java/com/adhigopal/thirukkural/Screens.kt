package com.adhigopal.thirukkural

import android.content.Intent
import android.net.Uri
import android.text.method.LinkMovementMethod
import android.util.TypedValue
import android.widget.ScrollView
import android.widget.TextView
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.text.HtmlCompat

private fun stripQuotes(s: String) = s.trim().trim('“', '”', '"')

// ---------- Static pages (Home / Learn More / Historical Texts) ----------

@Composable
fun HtmlPage(html: String) {
    AndroidView(
        modifier = Modifier.fillMaxSize().background(Paper),
        factory = { ctx ->
            val tv = TextView(ctx).apply {
                setPadding(48, 48, 48, 96)
                setTextSize(TypedValue.COMPLEX_UNIT_SP, 16f)
                setTextColor(android.graphics.Color.parseColor("#1F1F1F"))
                setLinkTextColor(Accent.toArgb())
                setLineSpacing(0f, 1.25f)
                setTextIsSelectable(true)
                movementMethod = LinkMovementMethod.getInstance()
                text = HtmlCompat.fromHtml(html, HtmlCompat.FROM_HTML_MODE_COMPACT)
            }
            ScrollView(ctx).apply {
                setBackgroundColor(Paper.toArgb())
                addView(tv)
            }
        },
    )
}

// ---------- The Kurals hub ----------

@Composable
fun KuralsHubScreen(d: AppData, openChapter: (Int) -> Unit, openKural: (Int) -> Unit) {
    var query by rememberSaveable { mutableStateOf("") }
    var expanded by rememberSaveable { mutableStateOf(setOf<Int>()) }

    Column(Modifier.fillMaxSize().background(Paper)) {
        Text("The Kurals", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Accent,
            modifier = Modifier.padding(start = 16.dp, top = 16.dp, end = 16.dp))
        OutlinedTextField(
            value = query, onValueChange = { query = it }, singleLine = true,
            placeholder = { Text("Search chapters, kurals or meanings") },
            modifier = Modifier.fillMaxWidth().padding(16.dp),
        )
        LazyColumn(Modifier.fillMaxSize()) {
            if (query.isBlank()) {
                d.paals.forEach { paal ->
                    item(key = "paal-${paal.key}") {
                        Column(Modifier.padding(start = 16.dp, end = 16.dp, top = 18.dp, bottom = 6.dp)) {
                            Text("${paal.ta} · ${paal.en}", fontSize = 19.sp, fontWeight = FontWeight.Bold, color = Accent)
                            Text(paal.sub, fontSize = 13.sp, color = Muted, fontStyle = FontStyle.Italic)
                            HorizontalDivider(color = Line, modifier = Modifier.padding(top = 6.dp))
                        }
                    }
                    d.chaptersIn(paal.key).forEach { ch ->
                        item(key = "ch-${ch.n}") {
                            val open = ch.n in expanded
                            Row(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp),
                                verticalAlignment = Alignment.CenterVertically) {
                                Text(if (open) "▾" else "▸", color = Muted, fontSize = 18.sp,
                                    modifier = Modifier.width(26.dp).clickable {
                                        expanded = if (open) expanded - ch.n else expanded + ch.n
                                    })
                                Text("${ch.n}", color = Accent, modifier = Modifier.width(36.dp))
                                Column(Modifier.weight(1f).clickable { openChapter(ch.n) }) {
                                    Text(ch.en, fontWeight = FontWeight.SemiBold)
                                    Text(ch.ta, color = Muted, fontSize = 14.sp)
                                }
                            }
                            if (open) {
                                Column(Modifier.padding(start = 78.dp, end = 16.dp, bottom = 8.dp)) {
                                    d.kuralsIn(ch).forEach { k -> KuralPreviewRow(k) { openKural(k.n) } }
                                }
                            }
                        }
                    }
                }
            } else {
                val results = d.search(query)
                item {
                    Text("${results.size} result${if (results.size == 1) "" else "s"}", color = Muted,
                        modifier = Modifier.padding(horizontal = 16.dp))
                }
                items(results.take(200), key = { it.n }) { k ->
                    Column(Modifier.padding(horizontal = 16.dp)) { KuralPreviewRow(k) { openKural(k.n) } }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun KuralPreviewRow(k: Kural, onClick: () -> Unit) {
    Row(Modifier.fillMaxWidth().clickable(onClick = onClick).padding(vertical = 8.dp)) {
        Text("${k.n}", color = Accent, fontSize = 13.sp, modifier = Modifier.width(42.dp))
        Text(k.ta, fontSize = 15.sp)
    }
}

// ---------- Chapter page ----------

@Composable
fun ChapterScreen(d: AppData, n: Int, openChapter: (Int) -> Unit, openKural: (Int) -> Unit) {
    val ch = d.chapterByNumber[n] ?: return
    LazyColumn(Modifier.fillMaxSize().background(Paper).padding(horizontal = 16.dp)) {
        item {
            Column(Modifier.padding(vertical = 16.dp)) {
                Text(ch.en, fontSize = 26.sp, fontWeight = FontWeight.Bold, color = Accent)
                Text("${ch.ta} · ${ch.tr}", color = Muted)
                Text("Chapter ${ch.n} of 133 · Kurals ${ch.start}–${ch.end}", color = Muted, fontSize = 13.sp)
                Text("Tap a kural for its full breakdown.", modifier = Modifier.padding(top = 12.dp))
            }
        }
        items(d.kuralsIn(ch), key = { it.n }) { k ->
            KuralPreviewRow(k) { openKural(k.n) }
            HorizontalDivider(color = Line)
        }
        item {
            Row(Modifier.fillMaxWidth().padding(vertical = 16.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                if (ch.n > 1) TextButton(onClick = { openChapter(ch.n - 1) }) { Text("← Chapter ${ch.n - 1}") } else Spacer(Modifier)
                if (ch.n < 133) TextButton(onClick = { openChapter(ch.n + 1) }) { Text("Chapter ${ch.n + 1} →") }
            }
        }
    }
}

// ---------- Kural study page ----------

@Composable
fun KuralScreen(d: AppData, start: Int) {
    var number by rememberSaveable { mutableIntStateOf(start) }
    val k = d.kuralByNumber[number] ?: return
    val ch = d.chapterByNumber[k.chapterNumber] ?: return
    val cites = remember(number) { d.citationIndex(k) }
    val scroll = rememberScrollState()
    LaunchedEffect(number) { scroll.scrollTo(0) }
    val context = LocalContext.current

    SelectionContainer {
        Column(Modifier.fillMaxSize().background(Paper).verticalScroll(scroll).padding(16.dp)) {
            Text("Kural ${k.n}", fontSize = 30.sp, fontWeight = FontWeight.Bold, color = Accent)
            Text("${ch.en} · ${ch.tr} · ${ch.ta}", color = Muted, fontSize = 14.sp)
            Text(k.ta, fontSize = 22.sp, fontWeight = FontWeight.SemiBold, textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth().padding(top = 20.dp, bottom = 8.dp))
            Text(k.tr, fontStyle = FontStyle.Italic, color = Muted, textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth())

            SectionTitle("Meaning"); Body(k.meaning)
            SectionTitle("Elementary"); Body(k.elementary)
            SectionTitle("University"); Body(k.university)

            SectionTitle("Through the Lens of")
            d.traditions.forEach { t ->
                k.x[t.key]?.let { x ->
                    Column(Modifier.padding(vertical = 10.dp)) {
                        Text(t.label, fontWeight = FontWeight.Bold, color = Accent, fontSize = 17.sp)
                        Text(if (x.isQuote) "“${stripQuotes(x.q)}”" else stripQuotes(x.q),
                            fontStyle = if (x.isQuote) FontStyle.Italic else FontStyle.Normal,
                            modifier = Modifier.padding(top = 4.dp))
                        Text("— ${x.s}" + (cites[x.c]?.let { "  [$it]" } ?: ""), color = Muted, fontSize = 13.sp,
                            modifier = Modifier.padding(vertical = 4.dp))
                        Body(x.ex)
                        Text(x.tb, fontStyle = FontStyle.Italic, color = Muted, modifier = Modifier.padding(top = 4.dp))
                    }
                }
            }

            val r = k.rle
            if (d.hasRealLifeExample && r != null) {
                SectionTitle("Real Life Example")
                Text(r.title, fontWeight = FontWeight.Bold, color = Accent, fontSize = 17.sp)
                Text(listOf(r.date, r.place).filter { it.isNotBlank() }.joinToString(" · "),
                    fontStyle = FontStyle.Italic, color = Muted, fontSize = 13.sp)
                Body(r.event)
                Text("— Sources: " + r.c.mapNotNull { cites[it]?.let { i -> "[$i]" } }.joinToString(" "),
                    color = Muted, fontSize = 13.sp, modifier = Modifier.padding(vertical = 4.dp))
                Body(r.ex)
                Text(r.tb, fontStyle = FontStyle.Italic, color = Muted, modifier = Modifier.padding(top = 4.dp))
            }

            SectionTitle("Sources for this page")
            cites.forEach { (cid, i) ->
                val s = d.sources[cid]
                val label = "$i. ${s?.title ?: cid}" + (s?.by?.takeIf { it.isNotBlank() }?.let { " ($it)" } ?: "")
                val url = s?.url.orEmpty()
                Text(label, fontSize = 13.sp, color = if (url.isNotBlank()) Accent else Muted,
                    modifier = Modifier.padding(vertical = 3.dp).let { m ->
                        if (url.isNotBlank()) m.clickable {
                            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
                        } else m
                    })
            }

            HorizontalDivider(color = Line, modifier = Modifier.padding(top = 20.dp))
            Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                if (k.n > 1) TextButton(onClick = { number = k.n - 1 }) { Text("← Kural ${k.n - 1}") } else Spacer(Modifier)
                if (k.n < 1330) TextButton(onClick = { number = k.n + 1 }) { Text("Kural ${k.n + 1} →") }
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically) {
                Text(ch.en, color = Muted, fontSize = 13.sp, modifier = Modifier.weight(1f))
                d.chapterByNumber[ch.n + 1]?.let { next ->
                    OutlinedButton(onClick = { number = next.start }) { Text("Skip to Next Chapter →") }
                }
            }
            Spacer(Modifier.height(32.dp))
        }
    }
}

@Composable
private fun SectionTitle(title: String) {
    Column(Modifier.padding(top = 22.dp, bottom = 8.dp)) {
        Text(title.uppercase(), color = Accent, fontWeight = FontWeight.Bold, fontSize = 12.sp, letterSpacing = 1.5.sp)
        HorizontalDivider(color = Line, modifier = Modifier.padding(top = 4.dp))
    }
}

@Composable
private fun Body(text: String) {
    Text(text, fontSize = 16.sp, lineHeight = 24.sp)
}
