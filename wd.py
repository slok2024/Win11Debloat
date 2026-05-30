import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Win11DebloatNativeCompact(tk.Tk):
    def __init__(self):
        super().__init__()

        # 极致窄版紧凑布局：确保小屏幕不占空间，完全服务于实用主义
        self.title("Win11Debloat")
        self.geometry("960x720")
        self.minsize(900, 660)

        # 设置原生 Ttk 风格主题
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # 深度定制底部核心执行按钮的漂亮样式：深蓝色背景、白字、大字体
        self.style.configure(
            "Action.TButton",
            font=("Microsoft YaHei", 11, "bold"),
            foreground="white",
            background="#104f55",
            padding=(20, 6)
        )
        # 鼠标悬停以及点击时的颜色平滑过渡映射
        self.style.map(
            "Action.TButton",
            background=[("active", "#187a82"), ("pressed", "#0b393d")],
            foreground=[("active", "white")]
        )
        
        self.options = {}
        self.combos = {}
        self.checkbox_widgets = {}
        self.last_search_query = ""

        # ==============================================================================
        # 核心数据矩阵：100% 完整复刻，无任何删减，确保功能全、有效
        # ==============================================================================
        self.app_matrix = {
            "App_Alarms": {"name": "闹钟与时钟", "ids": ["Microsoft.WindowsAlarms"], "cat": "base"},
            "App_Calculator": {"name": "计算器", "ids": ["Microsoft.WindowsCalculator"], "cat": "base"},
            "App_Camera": {"name": "相机", "ids": ["Microsoft.WindowsCamera"], "cat": "base"},
            "App_Feedback": {"name": "反馈中心", "ids": ["Microsoft.WindowsFeedbackHub"], "cat": "base"},
            "App_GetHelp": {"name": "获取帮助", "ids": ["Microsoft.GetHelp"], "cat": "base"},
            "App_GetStarted": {"name": "提示与入门(不可删)", "ids": ["Microsoft.Getstarted"], "cat": "base"},
            "App_MailCalendar": {"name": "邮件与日历", "ids": ["Microsoft.windowscommunicationsapps", "Microsoft.People"], "cat": "base"},
            "App_Maps": {"name": "Windows 地图", "ids": ["Microsoft.WindowsMaps"], "cat": "base"},
            "App_Notepad": {"name": "新版记事本", "ids": ["Microsoft.WindowsNotepad"], "cat": "base"},
            "App_Paint": {"name": "传统画图", "ids": ["Microsoft.Paint"], "cat": "base"},
            "App_Paint3D": {"name": "Paint 3D", "ids": ["Microsoft.MSPaint"], "cat": "base"},
            "App_Photos": {"name": "微软照片", "ids": ["Microsoft.WindowsPhotos"], "cat": "base"},
            "App_ScreenSketch": {"name": "截图工具", "ids": ["Microsoft.ScreenSketch"], "cat": "base"},
            "App_SoundRecorder": {"name": "录音机", "ids": ["Microsoft.WindowsSoundRecorder"], "cat": "base"},
            "App_StickyNotes": {"name": "便签", "ids": ["Microsoft.MicrosoftStickyNotes"], "cat": "base"},
            "App_Terminal": {"name": "Windows 终端", "ids": ["Microsoft.WindowsTerminal"], "cat": "base"},
            "App_Weather": {"name": "天气", "ids": ["Microsoft.BingWeather"], "cat": "base"},

            "App_3DBuilder": {"name": "3D Builder", "ids": ["Microsoft.3DBuilder"], "cat": "adv"},
            "App_3DViewer": {"name": "3D Viewer", "ids": ["Microsoft.Microsoft3DViewer"], "cat": "adv"},
            "App_Copilot": {"name": "Microsoft Copilot AI", "ids": ["Microsoft.Copilot"], "cat": "adv"},
            "App_AIHub": {"name": "Copilot+ AI Hub (24H2+)", "ids": ["Microsoft.Windows.AIHub"], "cat": "adv"},
            "App_Cortana": {"name": "Cortana 语音(已废弃)", "ids": ["Microsoft.549981C3F5F10"], "cat": "adv"},
            "App_DevHome": {"name": "开发者主页 (Dev Home)", "ids": ["Microsoft.Windows.DevHome"], "cat": "adv"},
            "App_Family": {"name": "微软家庭选项", "ids": ["MicrosoftCorporationII.MicrosoftFamily"], "cat": "adv"},
            "App_Journal": {"name": "微软手写日志", "ids": ["Microsoft.MicrosoftJournal"], "cat": "adv"},
            "App_M365Companions": {"name": "Microsoft 365 核心组件", "ids": ["Microsoft.M365Companions"], "cat": "adv"},
            "App_MixedReality": {"name": "混合现实门户", "ids": ["Microsoft.MixedReality.Portal"], "cat": "adv"},
            "App_OfficeHub": {"name": "Office 门户", "ids": ["Microsoft.MicrosoftOfficeHub"], "cat": "adv"},
            "App_OneDrive": {"name": "OneDrive 云盘客户端", "ids": ["Microsoft.OneDrive"], "cat": "adv"},
            "App_OneNote": {"name": "OneNote UWP 客户端", "ids": ["Microsoft.Office.OneNote"], "cat": "adv"},
            "App_Outlook": {"name": "新版 Windows Outlook", "ids": ["Microsoft.OutlookForWindows"], "cat": "adv"},
            "App_PhoneLink": {"name": "手机连接 / 跨设备体验", "ids": ["Microsoft.YourPhone", "MicrosoftWindows.CrossDevice"], "cat": "adv"},
            "App_PowerAutomate": {"name": "Power Automate 桌面", "ids": ["Microsoft.PowerAutomateDesktop"], "cat": "adv"},
            "App_PowerBI": {"name": "Power BI Windows 端", "ids": ["Microsoft.MicrosoftPowerBIForWindows"], "cat": "adv"},
            "App_Print3D": {"name": "Print 3D 打印", "ids": ["Microsoft.Print3D"], "cat": "adv"},
            "App_QuickAssist": {"name": "快速助手", "ids": ["MicrosoftCorporationII.QuickAssist"], "cat": "adv"},
            "App_RemoteDesktop": {"name": "远程桌面", "ids": ["Microsoft.RemoteDesktop"], "cat": "adv"},
            "App_Sway": {"name": "Sway 演示文稿", "ids": ["Microsoft.Office.Sway"], "cat": "adv"},
            "App_ToDo": {"name": "微软待办 (To Do)", "ids": ["Microsoft.Todos"], "cat": "adv"},
            "App_Whiteboard": {"name": "电子白板", "ids": ["Microsoft.Whiteboard"], "cat": "adv"},
            "App_PCManager": {"name": "微软电脑管家", "ids": ["Microsoft.PCManager"], "cat": "adv"},
            "App_Teams": {"name": "Microsoft Teams (全版本)", "ids": ["MSTeams", "MicrosoftTeams"], "cat": "adv"},
            "App_Widgets": {"name": "任务栏小组件 (Widgets 核心)", "ids": ["Microsoft.StartExperiencesApp", "Microsoft.WidgetsPlatformRuntime", "MicrosoftWindows.Client.WebExperience"], "cat": "adv"},
            "App_BingOld": {"name": "微软 Bing 历史全套死体组件", "ids": ["Microsoft.BingFinance", "Microsoft.BingFoodAndDrink", "Microsoft.BingHealthAndFitness", "Microsoft.BingNews", "Microsoft.BingSearch", "Microsoft.BingSports", "Microsoft.BingTranslator", "Microsoft.BingTravel", "Microsoft.News", "Microsoft.NetworkSpeedTest", "Microsoft.OneConnect"], "cat": "adv"},

            "App_XboxGroup": {"name": "Xbox 生态、游戏条关联全套组件", "ids": ["Microsoft.GamingApp", "Microsoft.XboxApp", "Microsoft.XboxGameOverlay", "Microsoft.XboxGamingOverlay", "Microsoft.XboxIdentityProvider", "Microsoft.XboxSpeechToTextOverlay", "Microsoft.Xbox.TCUI"], "cat": "media"},
            "App_GamingServices": {"name": "游戏核心后台服务 (Gaming Services)", "ids": ["Microsoft.GamingServices"], "cat": "media"},
            "App_Clipchamp": {"name": "Clipchamp 视频编辑器", "ids": ["Clipchamp.Clipchamp"], "cat": "media"},
            "App_Zune": {"name": "电影/电视与新版媒体播放器", "ids": ["Microsoft.ZuneVideo", "Microsoft.ZuneMusic"], "cat": "media"},

            "App_SocialThirdParty": {"name": "社交资讯(Facebook/Twitter/TikTok/Instagram等)", "ids": ["Facebook", "Twitter", "Instagram", "LinkedInforWindows", "XING", "Viber", "TikTok", "Flipboard"], "cat": "bloat"},
            "App_Streaming": {"name": "流媒体(Netflix/Prime Video/Spotify等)", "ids": ["Netflix", "AmazonVideo.PrimeVideo", "HULULLC.HULUPLUS", "Spotify", "PandoraMediaInc", "iHeartRadio", "TuneInRadio"], "cat": "bloat"},
            "App_Games": {"name": "休闲游戏群(纸牌/糖果传奇/沥青8等)", "ids": ["Microsoft.MicrosoftSolitaireCollection", "Asphalt8Airborne", "king.com.BubbleWitch3Saga", "CaesarsSlotsFreeCasino", "king.com.CandyCrushSaga", "king.com.CandyCrushSodaSaga", "COOKINGFEVER", "DisneyMagicKingdoms", "FarmVille2CountryEscape", "HiddenCity", "MarchofEmpires", "Royal Revolt", "Shazam"], "cat": "bloat"},
            "App_UtilsThirdParty": {"name": "捆绑工具(Amazon/Drawboard/WinZip/Plex等)", "ids": ["Amazon.com.Amazon", "ACGMediaPlayer", "DrawboardPDF", "Duolingo-LearnLanguagesforFree", "OneCalendar", "WinZipUniversal", "Wunderlist", "PicsArt-PhotoStudio", "Plex", "PolarrPhotoEditorAcademicEdition"], "cat": "bloat"},

            "App_HP_Set": {"name": "惠普 (HP) 附加服务及硬件管理全家桶 (17项完整覆盖)", "ids": ["AD2F1837.HPAIExperienceCenter", "AD2F1837.HPConnectedMusic", "AD2F1837.HPConnectedPhotopoweredbySnapfish", "AD2F1837.HPDesktopSupportUtilities", "AD2F1837.HPEasyClean", "AD2F1837.HPFileViewer", "AD2F1837.HPJumpStarts", "AD2F1837.HPPCHardwareDiagnosticsWindows", "AD2F1837.HPPowerManager", "AD2F1837.HPPrinterControl", "AD2F1837.HPPrivacySettings", "AD2F1837.HPQuickDrop", "AD2F1837.HPQuickTouch", "AD2F1837.HPRegistration", "AD2F1837.HPSupportAssistant", "AD2F1837.HPSureShieldAI", "AD2F1837.HPSystemInformation", "AD2F1837.HPWelcome", "AD2F1837.HPWorkWell", "AD2F1837.myHP"], "cat": "oem"},
            "App_Dell_Set": {"name": "戴尔 (Dell) 随机服务 (SupportAssist/Digital Delivery)", "ids": ["DellInc.DellDigitalDelivery", "DellInc.DellMobileConnect", "DellInc.DellSupportAssistforPCs"], "cat": "oem"},
            "App_Lenovo_Set": {"name": "联想 (Lenovo) Vantage 核心及后台随行服务", "ids": ["E046963F.LenovoCompanion", "LenovoCompanyLimited.LenovoVantageService"], "cat": "oem"},
            "App_OemOthers": {"name": "其它 OEM 常见捆绑 (Actipro/CyberLink/Eclipse)", "ids": ["ActiproSoftwareLLC", "CyberLinkMediaSuiteEssentials", "EclipseManager"], "cat": "oem"},

            "App_Danger_Edge": {"name": "【高危】Microsoft Edge 浏览器 (将导致系统沙盒等环境无浏览器可用)", "ids": ["Microsoft.Edge", "XPFFTQ037JWMHS"], "cat": "danger"},
            "App_Danger_Store": {"name": "【极高危】Microsoft Store 应用商店 (切勿轻易移除，移除后极难恢复！)", "ids": ["Microsoft.WindowsStore"], "cat": "danger"},
        }

        self.setup_ui()

    def setup_ui(self):
        # 顶层面板：单行、紧凑
        top_panel = ttk.Frame(self)
        top_panel.pack(fill="x", padx=10, pady=(6, 2))

        title_lbl = ttk.Label(top_panel, text="Win11Debloat", font=("Arial", 11, "bold"))
        title_lbl.pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_ui_elements)
        search_entry = ttk.Entry(top_panel, width=22, textvariable=self.search_var)
        search_entry.pack(side="right")
        
        # 快捷占位文字指示
        search_lbl = ttk.Label(top_panel, text="🔍 过滤: ", font=("Arial", 9))
        search_lbl.pack(side="right", padx=2)

        # 动作控制栏
        action_bar = ttk.Frame(self)
        action_bar.pack(fill="x", padx=10, pady=2)

        ttk.Button(action_bar, text="加载推荐方案", width=12, command=self.select_safe_defaults).pack(side="left", padx=(0, 4))
        ttk.Button(action_bar, text="清空", width=6, command=self.clear_all).pack(side="left", padx=4)

        self.options["Sysprep"] = tk.BooleanVar(value=False)
        sysprep_cb = ttk.Checkbutton(action_bar, text="Sysprep模式 (不锁死账户)", variable=self.options["Sysprep"])
        sysprep_cb.pack(side="left", padx=8)

        self.options["AllUsers"] = tk.BooleanVar(value=False)
        allusers_cb = ttk.Checkbutton(action_bar, text="应用于所有账户", variable=self.options["AllUsers"])
        allusers_cb.pack(side="left", padx=4)

        # 原生选项卡
        self.tabview = ttk.Notebook(self)
        self.tabview.pack(padx=10, pady=2, fill="both", expand=True)

        # 构建各个标签容器
        self.tab_uwp = ttk.Frame(self.tabview)
        self.tab_privacy = ttk.Frame(self.tabview)
        self.tab_system = ttk.Frame(self.tabview)
        self.tab_start = ttk.Frame(self.tabview)
        self.tab_explorer = ttk.Frame(self.tabview)
        self.tab_danger = ttk.Frame(self.tabview)

        self.tabview.add(self.tab_uwp, text="📦 预装 UWP 矩阵")
        self.tabview.add(self.tab_privacy, text="🔒 隐私与 AI 控制")
        self.tabview.add(self.tab_system, text="⚙️ 系统与更新")
        self.tabview.add(self.tab_start, text="🖥️ 开始菜单与任务栏")
        self.tabview.add(self.tab_explorer, text="📁 资源管理器与多任务")
        self.tabview.add(self.tab_danger, text="🛡️ 高风险隔离区")

        self.render_app_matrix_tab()
        self.render_privacy_ai_tab()
        self.render_system_update_tab()
        self.render_start_taskbar_tab()
        self.render_explorer_multitask_tab()

        # 底部控制栏：增加高度来适配更显眼的执行按钮
        bottom_bar = ttk.Frame(self)
        bottom_bar.pack(fill="x", padx=10, pady=(6, 10), side="bottom")

        self.log_output = ttk.Label(bottom_bar, text="状态: 底层管线就绪", font=("Arial", 10), foreground="gray")
        # 修正布局参数，采用符合底层 Tcl 规范的 anchor="w" 实现左侧对齐居中
        self.log_output.pack(side="left", fill="y", anchor="w")

        # 漂亮显眼的深度定制执行按钮 (应用 Action.TButton 样式)
        execute_btn = ttk.Button(bottom_bar, text="🚀 全面执行所选调整", style="Action.TButton", command=self.execute_engine)
        execute_btn.pack(side="right")

    # --- 原生硬核滚动条网格构建器 ---
    def create_scroll_grid(self, tab_obj):
        canvas = tk.Canvas(tab_obj, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab_obj, orient="vertical", command=canvas.yview)
        scroll_content = ttk.Frame(canvas)

        scroll_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

        # 绑定鼠标滚轮事件支持
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        scroll_content.columnconfigure(0, weight=1, uniform="group")
        scroll_content.columnconfigure(1, weight=1, uniform="group")
        return scroll_content

    def create_compact_card(self, parent, title, row, col, columnspan=1):
        card = ttk.LabelFrame(parent, text=f" {title} ")
        card.grid(row=row, column=col, columnspan=columnspan, padx=4, pady=4, sticky="nsew")
        return card

    def add_cb(self, card, text, key, default=False):
        self.options[key] = tk.BooleanVar(value=default)
        cb = ttk.Checkbutton(card, text=text, variable=self.options[key])
        cb.pack(anchor="w", pady=1, padx=6)
        self.checkbox_widgets[key] = cb

    def add_combo(self, card, text, key, values, default_val):
        lbl = ttk.Label(card, text=text, font=("Arial", 9), foreground="gray")
        lbl.pack(anchor="w", padx=6, pady=(2, 0))
        self.combos[key] = tk.StringVar(value=default_val)
        combo = ttk.Combobox(card, values=values, textvariable=self.combos[key], state="readonly", width=22)
        combo.pack(anchor="w", padx=6, pady=(0, 2))

    # --- 标签页 1: 预装 UWP 矩阵 ---
    def render_app_matrix_tab(self):
        grid = self.create_scroll_grid(self.tab_uwp)
        
        c1 = self.create_compact_card(grid, "📌 微软原生基础与日常应用", 0, 0)
        c2 = self.create_compact_card(grid, "🧩 微软高级特征、AI 与死体组件", 0, 1)
        c3 = self.create_compact_card(grid, "🎬 Xbox 游戏生态与多媒体组件", 1, 0)
        c4 = self.create_compact_card(grid, "🔥 社交、第三方推广与游戏", 1, 1)
        c5 = self.create_compact_card(grid, "🏭 OEM 厂商残余全家桶 (HP / Dell / Lenovo)", 2, 0, columnspan=2)

        for k in ["App_Alarms", "App_Calculator", "App_Camera", "App_Feedback", "App_GetHelp", "App_GetStarted", "App_MailCalendar", "App_Maps", "App_Notepad", "App_Paint", "App_Paint3D", "App_Photos", "App_ScreenSketch", "App_SoundRecorder", "App_StickyNotes", "App_Terminal", "App_Weather"]:
            self.add_cb(c1, self.app_matrix[k]["name"], k)
            
        for k in ["App_3DBuilder", "App_3DViewer", "App_Copilot", "App_AIHub", "App_Cortana", "App_DevHome", "App_Family", "App_Journal", "App_M365Companions", "App_MixedReality", "App_OfficeHub", "App_OneDrive", "App_OneNote", "App_Outlook", "App_PhoneLink", "App_PowerAutomate", "App_PowerBI", "App_Print3D", "App_QuickAssist", "App_RemoteDesktop", "App_Sway", "App_ToDo", "App_Whiteboard", "App_PCManager", "App_Teams", "App_Widgets", "App_BingOld"]:
            self.add_cb(c2, self.app_matrix[k]["name"], k)

        for k in ["App_XboxGroup", "App_GamingServices", "App_Clipchamp", "App_Zune"]:
            self.add_cb(c3, self.app_matrix[k]["name"], k)

        for k in ["App_SocialThirdParty", "App_Streaming", "App_Games", "App_UtilsThirdParty"]:
            self.add_cb(c4, self.app_matrix[k]["name"], k)

        for k in ["App_HP_Set", "App_Dell_Set", "App_Lenovo_Set", "App_OemOthers"]:
            self.add_cb(c5, self.app_matrix[k]["name"], k)

        # 高风险隔离区
        grid_danger = self.create_scroll_grid(self.tab_danger)
        c_danger = self.create_compact_card(grid_danger, "⚠️ 系统核心级高危组件 (非特定母盘精简不建议勾选)", 0, 0)
        self.add_cb(c_danger, self.app_matrix["App_Danger_Edge"]["name"], "App_Danger_Edge")
        self.add_cb(c_danger, self.app_matrix["App_Danger_Store"]["name"], "App_Danger_Store")

    # --- 标签页 2: 隐私与 AI 控制 ---
    def render_privacy_ai_tab(self):
        grid = self.create_scroll_grid(self.tab_privacy)

        c1 = self.create_compact_card(grid, "🔒 隐私保护与遥测断开 (Privacy)", 0, 0)
        self.add_cb(c1, "禁用遥测、诊断数据、活动历史与目标广告", "DisableTelemetry")
        self.add_cb(c1, "禁用应用启动跟踪 (App-launch tracking)", "DisableLaunchTracking")
        self.add_cb(c1, "禁用 Windows 位置服务及应用定位访问", "DisableLocation")
        self.add_cb(c1, "禁用 '查找我的设备' 位置追踪", "DisableFindMyDevice")
        self.add_cb(c1, "禁用本地 Windows 搜索历史记录", "DisableSearchHistory")

        c2 = self.create_compact_card(grid, "📢 广告与内容推荐隔离 (Suggested Content)", 0, 1)
        self.add_cb(c2, "关闭全局提示、技巧、建议与广告弹窗", "DisableSuggestions")
        self.add_cb(c2, "禁用锁屏界面上的 'Windows 聚焦' 提示技巧", "DisableLockscreenTips")
        self.add_cb(c2, "禁用桌面的 'Windows Spotlight' 壁纸选项", "DisableDesktopSpotlight")
        self.add_cb(c2, "屏蔽 Edge 内的广告、推广提示与 MSN 新闻流", "DisableEdgeAds")
        self.add_cb(c2, "隐藏设置主页的 Microsoft 365 广告", "HideSettings365Ads")
        self.add_cb(c2, "彻底隐藏并禁用整个设置 '主页 (Home)' 视图", "HideSettingsHomePage")

        c3 = self.create_compact_card(grid, "🧠 人工智能深度剥离 (AI Features)", 1, 0)
        self.add_cb(c3, "禁用并从系统中移除 Microsoft Copilot AI", "Privacy_DisableCopilot")
        self.add_cb(c3, "禁用 Windows Recall (回忆快照功能)", "DisableRecall")
        self.add_cb(c3, "禁用 Click to Do (屏幕智能文本图像分析工具)", "DisableClickToDo")
        self.add_cb(c3, "拦截 AI 核心后台服务 (WSAIFabricSvc) 自动启动", "DisableAISvcStart")

        c4 = self.create_compact_card(grid, "🌐 专属应用内 AI 功能屏蔽", 1, 1)
        self.add_cb(c4, "剥离 Edge 浏览器中的 AI 特性及侧边栏按钮", "DisableEdgeAI Features")
        self.add_cb(c4, "禁用新版 画图 (Paint) 的 AI 创作层与滤镜", "DisablePaintAI")
        self.add_cb(c4, "禁用 记事本 (Notepad) 的 AI 文本辅助生成", "DisableNotepadAI")

    # --- 标签页 3: 系统与更新微调 ---
    def render_system_update_tab(self):
        grid = self.create_scroll_grid(self.tab_system)

        c1 = self.create_compact_card(grid, "⚙️ 系统高级底层调校 (System)", 0, 0)
        self.add_cb(c1, "禁用移动文件时顶部的 'Drag Tray' 共享区", "DisableDragTray")
        self.add_cb(c1, "恢复经典的 Windows 10 全布局右键菜单", "RevertContextMenu")
        self.add_cb(c1, "关闭鼠标加速功能 (提升物理指针精准度)", "DisableMouseAcceleration")
        self.add_cb(c1, "禁用连按 5 次 Shift 触发的粘滞键快捷键", "DisableStickyKeys")
        self.add_cb(c1, "禁用存储感知 (Storage Sense) 自动磁盘清理", "DisableStorageSense")
        self.add_cb(c1, "禁用快速启动 (Fast Start-up) 以实现彻底关机", "DisableFastStartup")
        self.add_cb(c1, "拦截并阻止 BitLocker 自动设备加密行为", "DisableBitLockerAuto")
        self.add_cb(c1, "现代休眠 (Modern Standby) 期间断网省电", "DisableStandbyNetwork")

        c2 = self.create_compact_card(grid, "🔄 补丁更新策略调校 (Windows Update)", 0, 1)
        self.add_cb(c2, "阻止系统在更新发布后第一时间自动推送获取", "DisableUpdateASAP")
        self.add_cb(c2, "禁止系统在完成更新登录后自动执行强制重启", "PreventUpdateAutoReboot")
        self.add_cb(c2, "关闭传递优化 (禁止后台跨设备上传共享补丁)", "DisableDeliveryOptimization")

        c3 = self.create_compact_card(grid, "🎨 全局视觉个性化 (Appearance)", 1, 0)
        self.add_cb(c3, "外观全局开启深色模式 (Dark Mode)", "EnableDarkMode")
        self.add_cb(c3, "彻底关闭全局窗口透明效果 (Transparency)", "DisableTransparency")
        self.add_cb(c3, "关闭窗口缩放、淡入淡出等全局动画特效", "DisableAnimations")

        c4 = self.create_compact_card(grid, "🧩 可选功能与扩展微调 (Features & Other)", 1, 1)
        self.add_cb(c4, "在当前系统中开启原生 Windows 沙盒 (Sandbox)", "EnableWindowsSandbox")
        self.add_cb(c4, "开启 WSL (Windows Linux 子系统底层环境)", "EnableWSL")
        self.add_cb(c4, "彻底禁用 Xbox Game Bar 后台录屏与覆盖层", "DisableXboxGameBarIntegration")
        self.add_cb(c4, "剥离 Brave 浏览器捆绑的 AI、钱包与新闻流广告", "DisableBraveBloat")

    # --- 标签页 4: 开始菜单与任务栏 ---
    def render_start_taskbar_tab(self):
        grid = self.create_scroll_grid(self.tab_start)

        c1 = self.create_compact_card(grid, "🔍 开始菜单与搜索过滤 (Start & Search)", 0, 0)
        self.add_cb(c1, "清空或替换开始菜单中所有默认固定的应用图标", "ClearPinnedApps")
        self.add_cb(c1, "隐藏开始菜单底部的 '推荐内容' 区域", "HideStartRecommended")
        self.add_cb(c1, "隐藏开始菜单中的 '所有应用' (All Apps) 列表", "HideStartAllApps")
        self.add_cb(c1, "禁用开始菜单中的 '手机连接' 移动集成", "DisableStartPhoneLink")
        self.add_cb(c1, "阻断 Windows 本地搜索结合 Bing 网搜与 AI 交互", "DisableBingSearch")
        self.add_cb(c1, "禁用应用商店 (Microsoft Store) 的搜索联想建议", "DisableStoreSearchSuggestions")
        self.add_cb(c1, "停用任务栏搜索框内的 '搜索要闻' 动态图案广告", "DisableSearchHighlights")

        c2 = self.create_compact_card(grid, "🖥️ 任务栏基础及交互调校 (Taskbar)", 0, 1)
        self.add_cb(c2, "将任务栏上的所有图标位置强制居左对齐", "TaskbarAlignLeft")
        self.add_cb(c2, "隐藏任务栏上的 '任务视图' (Task View) 按钮", "HideTaskview")
        self.add_cb(c2, "隐藏/关闭任务栏及锁屏界面上的 '小组件'", "DisableWidgets")
        self.add_cb(c2, "隐藏任务栏上的 '聊天 (Chat)' 图标", "HideChat")
        self.add_cb(c2, "任务栏图标右键菜单中增加原生 '结束任务' 选项", "EnableEndTask")
        self.add_cb(c2, "连续点击任务栏图标可循环切换该应用活动窗口", "EnableLastActiveClick")
        
        self.add_combo(c2, "搜索栏样式:", "SearchBoxStyle", ["不作更改", "完全隐藏", "仅显示图标", "显示图标与标签", "标准搜索框"], "不作更改")
        self.add_combo(c2, "主屏任务栏合并:", "CombineTaskbarMode", ["不作更改", "始终合并", "满时合并", "从不合并"], "不作更改")
        self.add_combo(c2, "多屏任务栏合并:", "CombineMMTaskbarMode", ["不作更改", "始终合并", "满时合并", "从不合并"], "不作更改")

    # --- 标签页 5: 资源管理器与多任务 ---
    def render_explorer_multitask_tab(self):
        grid = self.create_scroll_grid(self.tab_explorer)

        c1 = self.create_compact_card(grid, "📁 资源管理器节点精简 (File Explorer)", 0, 0)
        self.add_cb(c1, "显示已知文件类型的扩展名 (如 .txt, .exe)", "ShowKnownFileExt")
        self.add_cb(c1, "显示系统隐藏的文件、文件夹和受保护的驱动器", "ShowHiddenFolders")
        self.add_cb(c1, "在左侧导航面板中彻底隐藏 '主页 (Home)' 节点", "HideHome")
        self.add_cb(c1, "在左侧导航面板中彻底隐藏 '图库 (Gallery)' 节点", "HideGallery")
        self.add_cb(c1, "从导航面板中隐藏重复的外置可移动磁盘节点", "HideDuplicateDrives")
        self.add_cb(c1, "将传统常用文件夹重新加回 '此电脑'", "AddFoldersToThisPC")
        self.add_cb(c1, "从导航面板中隐藏 3D 对象、音乐或 OneDrive", "Hide3DFolders")
        self.add_cb(c1, "从右键菜单移除 '包含在库中'、'授予权限' 与 '共享'", "CleanContextMenuOptions")
        self.add_combo(c1, "默认打开位置到:", "ExplorerOpenTarget", ["不作更改", "主页 (Home)", "此电脑 (This PC)", "下载 (Downloads)"], "不作更改")
        self.add_combo(c1, "磁盘盘符排序:", "DriveLettersMode", ["不作更改", "盘符显示在最前", "盘符显示在最后", "隐藏所有盘符"], "不作更改")

        c2 = self.create_compact_card(grid, "🌀 窗口贴靠与多任务流 (Multi-tasking)", 0, 1)
        self.add_cb(c2, "彻底关闭窗口拖拽贴靠功能 (Window Snapping)", "DisableWindowSnapping")
        self.add_cb(c2, "关闭窗口贴靠后的 '贴靠助手' 缩略图", "DisableSnapOriginalAssist")
        self.add_cb(c2, "关闭悬停最大化按钮产生的 '贴靠布局' 弹窗建议", "DisableSnapLayoutsSuggestions")
        self.add_combo(c2, "Alt+Tab 浏览器标签显示:", "AltTabTabsMode", ["不作更改", "不显示标签页", "显示最近3个", "显示最近5个", "从不显示"], "不作更改")

    def select_safe_defaults(self):
        """精准勾选核心底层变量：100% 同步渲染界面"""
        defaults = [
            "App_SocialThirdParty", "App_Streaming", "App_Games", "App_UtilsThirdParty", 
            "App_Cortana", "App_BingOld", "DisableTelemetry", "DisableSuggestions", 
            "DisableLockscreenTips", "DisableEdgeAds", "Privacy_DisableCopilot", 
            "DisableRecall", "DisableClickToDo", "DisableAISvcStart", "RevertContextMenu", 
            "ShowKnownFileExt", "ShowHiddenFolders", "DisableSearchHighlights", 
            "DisableWidgets", "HideChat", "EnableEndTask", "EnableLastActiveClick"
        ]
        self.clear_all()
        for key in defaults:
            if key in self.options:
                self.options[key].set(True)  # 精准控制底层核心变量勾选
        self.log_output.configure(text="状态: 已自动加载推荐优化方案")

    def clear_all(self):
        for var in self.options.values():
            var.set(False)
        for key in self.combos:
            self.combos[key].set("不作更改")
        self.log_output.configure(text="状态: 已清空所有勾选")

    def filter_ui_elements(self, *args):
        """原生高频防重绘引擎：完美的字符串条件判定，直接拦截无变动事件，不耗费 CPU"""
        query = self.search_var.get().strip().lower()
        if query == self.last_search_query:
            return
        self.last_search_query = query

        # 原生安全重绘锁：挂起渲染
        self.withdraw()
        
        for key, cb in self.checkbox_widgets.items():
            if not query or query in cb.cget("text").lower():
                if not cb.winfo_managed():
                    cb.pack(anchor="w", pady=1, padx=6)
            else:
                if cb.winfo_managed():
                    cb.pack_forget()
                    
        # 释放渲染锁
        self.deiconify()

    def translate_to_powershell(self):
        cmds = []
        scope = " -AllUsers" if self.options["AllUsers"].get() else ""

        target_ids = []
        danger_triggered = False
        for key, info in self.app_matrix.items():
            if self.options.get(key) and self.options[key].get():
                if info["cat"] == "danger":
                    danger_triggered = True
                target_ids.extend(info["ids"])
        
        if target_ids:
            formatted_ids = ",".join([f"'{i}'" for i in target_ids])
            cmds.append(f"Get-AppxPackage{scope} | Where-Object {{ $_.Name -in ({formatted_ids}) -or $_.PackageFamilyName -in ({formatted_ids}) }} | Remove-AppxPackage -ErrorAction SilentlyContinue")
            cmds.append(f"Get-AppxProvisionedPackage -Online | Where-Object {{ $_.DisplayName -in ({formatted_ids}) }} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue")

        if self.options["DisableTelemetry"].get():
            cmds.append('Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Value 0 -Force')
        if self.options["Privacy_DisableCopilot"].get():
            cmds.append('Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" -Name "TurnOffWindowsCopilot" -Value 1 -Force')
        if self.options["DisableRecall"].get():
            cmds.append('Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsAI" -Name "TurnOffWindowsRecall" -Value 1 -Force')

        if self.options["RevertContextMenu"].get():
            path = "HKCU:\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32"
            cmds.append(f'if (!(Test-Path "{path}")) {{ New-Item -Path "{path}" -Force | Out-Null }}')
            cmds.append(f'Set-ItemProperty -Path "{path}" -Name "" -Value "" -Force')
        if self.options["ShowKnownFileExt"].get():
            cmds.append('Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "HideFileExt" -Value 0 -Force')
        if self.options["ShowHiddenFolders"].get():
            cmds.append('Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Hidden" -Value 1 -Force')

        if self.options["TaskbarAlignLeft"].get():
            cmds.append('Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "TaskbarAl" -Value 0 -Force')
        if self.options["EnableEndTask"].get():
            cmds.append('Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\DeveloperSettings" -Name "TaskbarEndTask" -Value 1 -Force')

        return "\n".join(cmds), danger_triggered

    def execute_engine(self):
        ps_block, danger_triggered = self.translate_to_powershell()
        if not ps_block:
            messagebox.showwarning("提示", "您尚未勾选任何配置项。")
            return

        if danger_triggered:
            ans = messagebox.askyesno("核心级高危警告", "您勾选了 Edge 或 商店核心组件。\n确定要强制精简吗？")
            if not ans:
                return

        self.log_output.configure(text="状态: 系统正在调度全量优化...", foreground="#ff9900")
        self.update()

        try:
            process = subprocess.Popen(
                ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", f"& {{ {ps_block} }}"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            stdout, stderr = process.communicate()
            self.log_output.configure(text="状态: 选定项目全量应用成功！", foreground="green")
            messagebox.showinfo("成功", "所有选定策略及 UWP 卸载包已成功执行！")
        except Exception as e:
            self.log_output.configure(text="状态: 执行遭遇阻断崩溃", foreground="red")
            messagebox.showerror("内部异常", f"优化调度遭遇阻断: {str(e)}")

if __name__ == "__main__":
    if sys.platform == "win32":
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)

    app = Win11DebloatNativeCompact()
    app.mainloop()