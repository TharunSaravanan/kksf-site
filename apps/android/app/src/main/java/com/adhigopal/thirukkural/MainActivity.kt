package com.adhigopal.thirukkural

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

val Accent = Color(0xFF8A4B00)
val Paper = Color(0xFFFFFDF8)
val Line = Color(0xFFE8E0D2)
val Muted = Color(0xFF6B6B6B)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(colorScheme = lightColorScheme(primary = Accent, background = Paper, surface = Paper)) {
                AppRoot()
            }
        }
    }
}

private data class Tab(val route: String, val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)

private val TABS = listOf(
    Tab("home", "Home", Icons.Filled.Home),
    Tab("kurals", "The Kurals", Icons.Filled.List),
    Tab("learn", "Learn More", Icons.Filled.Info),
    Tab("texts", "Historical Texts", Icons.Filled.Star),
)

@Composable
fun AppRoot() {
    val context = LocalContext.current
    var data by remember { mutableStateOf<AppData?>(null) }
    LaunchedEffect(Unit) {
        data = withContext(Dispatchers.IO) { AppData.load(context.applicationContext) }
    }
    val d = data
    if (d == null) {
        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator(color = Accent) }
        return
    }

    val nav = rememberNavController()
    val backStack by nav.currentBackStackEntryAsState()
    val current = backStack?.destination?.route

    Scaffold(
        containerColor = Paper,
        bottomBar = {
            NavigationBar(containerColor = Paper) {
                TABS.forEach { tab ->
                    val selected = current == tab.route ||
                        (tab.route == "kurals" && (current?.startsWith("chapter") == true || current?.startsWith("kural/") == true))
                    NavigationBarItem(
                        selected = selected,
                        onClick = {
                            nav.navigate(tab.route) {
                                popUpTo("home") { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        icon = { Icon(tab.icon, contentDescription = tab.label) },
                        label = { Text(tab.label, maxLines = 1) },
                    )
                }
            }
        },
    ) { padding ->
        NavHost(nav, startDestination = "home", modifier = Modifier.padding(padding)) {
            composable("home") { HtmlPage(d.pageHome) }
            composable("learn") { HtmlPage(d.pageLearnMore) }
            composable("texts") { HtmlPage(d.pageHistoricalTexts) }
            composable("kurals") {
                KuralsHubScreen(d,
                    openChapter = { nav.navigate("chapter/$it") },
                    openKural = { nav.navigate("kural/$it") })
            }
            composable("chapter/{n}", arguments = listOf(navArgument("n") { type = NavType.IntType })) { entry ->
                val n = entry.arguments?.getInt("n") ?: 1
                ChapterScreen(d, n,
                    openChapter = { nav.navigate("chapter/$it") },
                    openKural = { nav.navigate("kural/$it") })
            }
            composable("kural/{n}", arguments = listOf(navArgument("n") { type = NavType.IntType })) { entry ->
                val n = entry.arguments?.getInt("n") ?: 1
                KuralScreen(d, n)
            }
        }
    }
}
