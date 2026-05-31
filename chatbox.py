import http.server
import socketserver
import webbrowser
import threading
import time
import sys

# HTML Content of the optimized chatbot
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aether AI Chatbot</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient-start: #e0e7ff;
            --bg-gradient-end: #e8eaf6;
            --container-bg: rgba(255, 255, 255, 0.45);
            --container-border: rgba(255, 255, 255, 0.4);
            --text-main: #1e293b;
            --text-muted: #64748b;
            --msg-user-bg: linear-gradient(135deg, #6366f1, #4f46e5);
            --msg-user-color: #ffffff;
            --msg-bot-bg: rgba(255, 255, 255, 0.6);
            --msg-bot-border: rgba(255, 255, 255, 0.5);
            --msg-bot-color: #1e293b;
            --input-bg: rgba(255, 255, 255, 0.5);
            --input-border: rgba(255, 255, 255, 0.6);
            --chip-bg: rgba(255, 255, 255, 0.6);
            --chip-hover-bg: rgba(255, 255, 255, 0.85);
            --chip-border: rgba(255, 255, 255, 0.5);
            --scrollbar-thumb: rgba(0, 0, 0, 0.1);
            --shadow-color: rgba(79, 70, 229, 0.1);
            --glow-color-1: rgba(99, 102, 241, 0.15);
            --glow-color-2: rgba(168, 85, 247, 0.15);
        }

        [data-theme="dark"] {
            --bg-gradient-start: #090d16;
            --bg-gradient-end: #0f172a;
            --container-bg: rgba(15, 23, 42, 0.65);
            --container-border: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --msg-user-bg: linear-gradient(135deg, #6366f1, #8b5cf6);
            --msg-user-color: #ffffff;
            --msg-bot-bg: rgba(30, 41, 59, 0.7);
            --msg-bot-border: rgba(255, 255, 255, 0.05);
            --msg-bot-color: #f8fafc;
            --input-bg: rgba(30, 41, 59, 0.5);
            --input-border: rgba(255, 255, 255, 0.05);
            --chip-bg: rgba(30, 41, 59, 0.6);
            --chip-hover-bg: rgba(30, 41, 59, 0.85);
            --chip-border: rgba(255, 255, 255, 0.05);
            --scrollbar-thumb: rgba(255, 255, 255, 0.1);
            --shadow-color: rgba(0, 0, 0, 0.4);
            --glow-color-1: rgba(99, 102, 241, 0.25);
            --glow-color-2: rgba(139, 92, 246, 0.25);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }

        body {
            background: linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
        }

        /* Decorative glowing blobs */
        .glow-blob {
            position: absolute;
            width: 450px;
            height: 450px;
            border-radius: 50%;
            filter: blur(120px);
            z-index: 0;
            pointer-events: none;
            animation: pulse-glow 15s infinite alternate ease-in-out;
        }

        .blob-1 {
            background: var(--glow-color-1);
            top: -100px;
            left: -100px;
        }

        .blob-2 {
            background: var(--glow-color-2);
            bottom: -150px;
            right: -100px;
            animation-delay: -5s;
        }

        @keyframes pulse-glow {
            0% { transform: scale(1) translate(0, 0); }
            50% { transform: scale(1.15) translate(30px, -20px); }
            100% { transform: scale(0.9) translate(-20px, 40px); }
        }

        .chat-container {
            width: 480px;
            max-width: 95vw;
            height: 720px;
            background: var(--container-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--container-border);
            border-radius: 28px;
            box-shadow: 0 25px 50px -12px var(--shadow-color);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            z-index: 1;
            position: relative;
        }

        .chat-header {
            padding: 20px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--container-border);
            background: rgba(255, 255, 255, 0.05);
        }

        .bot-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .bot-avatar-header {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 8px 16px rgba(99, 102, 241, 0.2);
        }

        .bot-avatar-header svg {
            width: 22px;
            height: 22px;
            fill: currentColor;
        }

        .bot-name-container {
            display: flex;
            flex-direction: column;
        }

        .bot-name {
            font-weight: 600;
            font-size: 16px;
            color: var(--text-main);
        }

        .bot-status {
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .status-dot {
            width: 7px;
            height: 7px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10b981;
            animation: pulse-dot 2s infinite;
        }

        @keyframes pulse-dot {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        .theme-toggle-btn {
            background: none;
            border: none;
            cursor: pointer;
            color: var(--text-main);
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--container-border);
            transition: all 0.2s ease;
        }

        .theme-toggle-btn:hover {
            transform: scale(1.05);
            background: rgba(255, 255, 255, 0.15);
        }

        .theme-toggle-btn svg {
            width: 18px;
            height: 18px;
            fill: none;
            stroke: currentColor;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        /* Chat area */
        .chat-box {
            flex-grow: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            scroll-behavior: smooth;
        }

        .chat-box::-webkit-scrollbar {
            width: 6px;
        }

        .chat-box::-webkit-scrollbar-track {
            background: transparent;
        }

        .chat-box::-webkit-scrollbar-thumb {
            background: var(--scrollbar-thumb);
            border-radius: 10px;
        }

        /* Messages */
        .message-wrapper {
            display: flex;
            align-items: flex-end;
            gap: 10px;
            max-width: 82%;
            animation: slide-up 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            opacity: 0;
            transform: translateY(16px);
        }

        @keyframes slide-up {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message-wrapper.user {
            margin-left: auto;
            flex-direction: row-reverse;
        }

        .message-wrapper.bot {
            margin-right: auto;
        }

        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            flex-shrink: 0;
        }

        .user .avatar {
            background: linear-gradient(135deg, #a855f7, #6366f1);
            display: none;
        }

        .bot .avatar {
            background: linear-gradient(135deg, #6366f1, #4f46e5);
        }

        .avatar svg {
            width: 18px;
            height: 18px;
            fill: currentColor;
        }

        .message-bubble {
            padding: 12px 18px;
            border-radius: 18px;
            font-size: 14.5px;
            line-height: 1.5;
            word-wrap: break-word;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
        }

        .user .message-bubble {
            background: var(--msg-user-bg);
            color: var(--msg-user-color);
            border-bottom-right-radius: 4px;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15);
        }

        .bot .message-bubble {
            background: var(--msg-bot-bg);
            border: 1px solid var(--msg-bot-border);
            color: var(--msg-bot-color);
            border-bottom-left-radius: 4px;
        }

        /* Typing indicator */
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 8px 14px;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            background-color: var(--text-muted);
            border-radius: 50%;
            opacity: 0.6;
            animation: typing-bounce 1.4s infinite ease-in-out both;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typing-bounce {
            0%, 80%, 100% { transform: scale(0.6); }
            40% { transform: scale(1.1) translateY(-4px); }
        }

        /* Suggestion chips */
        .suggestions-container {
            padding: 8px 20px;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            border-top: 1px solid var(--container-border);
            background: rgba(255, 255, 255, 0.01);
        }

        .suggestion-chip {
            background: var(--chip-bg);
            border: 1px solid var(--chip-border);
            color: var(--text-main);
            padding: 6px 14px;
            border-radius: 100px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            font-weight: 500;
        }

        .suggestion-chip:hover {
            background: var(--chip-hover-bg);
            transform: translateY(-1.5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        }

        .suggestion-chip:active {
            transform: translateY(0);
        }

        /* Input section */
        .input-area {
            padding: 16px 20px 20px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(255, 255, 255, 0.02);
        }

        .input-wrapper {
            flex-grow: 1;
            display: flex;
            align-items: center;
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 100px;
            padding: 4px 6px 4px 16px;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .input-wrapper:focus-within {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
        }

        input {
            flex-grow: 1;
            background: transparent;
            border: none;
            outline: none;
            padding: 10px 0;
            color: var(--text-main);
            font-size: 14.5px;
        }

        input::placeholder {
            color: var(--text-muted);
            opacity: 0.8;
        }

        .send-btn {
            background: linear-gradient(135deg, #6366f1, #4f46e5);
            color: white;
            border: none;
            cursor: pointer;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .send-btn:hover {
            transform: scale(1.05) rotate(5deg);
            background: linear-gradient(135deg, #4f46e5, #4338ca);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.35);
        }

        .send-btn:active {
            transform: scale(0.95);
        }

        .send-btn svg {
            width: 16px;
            height: 16px;
            fill: none;
            stroke: currentColor;
            stroke-width: 2.5;
            stroke-linecap: round;
            stroke-linejoin: round;
            transform: translate(1px, -0.5px);
        }
    </style>
</head>
<body>

<div class="glow-blob blob-1"></div>
<div class="glow-blob blob-2"></div>

<div class="chat-container">
    <div class="chat-header">
        <div class="bot-info">
            <div class="bot-avatar-header" id="botAvatarHeader"></div>
            <div class="bot-name-container">
                <span class="bot-name">Aether AI</span>
                <span class="bot-status">
                    <span class="status-dot"></span>
                    Online
                </span>
            </div>
        </div>
        <button class="theme-toggle-btn" id="themeToggle" onclick="toggleTheme()" aria-label="Toggle dark mode"></button>
    </div>

    <div class="chat-box" id="chatBox"></div>

    <div class="suggestions-container" id="suggestionsContainer"></div>

    <div class="input-area">
        <div class="input-wrapper">
            <input type="text" id="userInput" placeholder="Type a message..." autocomplete="off">
        </div>
        <button class="send-btn" onclick="sendMessage()" aria-label="Send message" id="sendBtn"></button>
    </div>
</div>

<script>
    // SVG strings
    const SVG_MOON = `<svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    const SVG_SUN = `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
    const SVG_BOT = `<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 1 10 10c0 5.523-4.477 10-10 10S2 17.523 2 12A10 10 0 0 1 12 2zm0 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-4-7a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm8 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/></svg>`;
    const SVG_USER = `<svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>`;
    const SVG_SEND = `<svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>`;

    // Bot Response Map
    const BOT_RESPONSES = {
        pacman: "Pacman AI uses search algorithms like BFS, DFS, A*, or state-evaluation heuristics to guide Pacman and the ghosts. In this project, pacman.py is a Pygame implementation where the player currently controls Pacman with the arrow keys. We could also add pathfinding AI for the ghosts!",
        python: "Here is a cool Python tip: You can use 'else' with a 'for' or 'while' loop! The 'else' block executes only if the loop completed naturally without hitting a 'break' statement. It's super useful for search operations!",
        project: "This chatbot is a local web application served via a secure Python HTTP server. It features an optimized modern UI with glassmorphism, responsive design, dark/light theme options, and XSS-protected inputs.",
        hello: "Hello there! I'm Aether, your AI assistant. How can I help you build or optimize today?",
        hi: "Hello there! I'm Aether, your AI assistant. How can I help you build or optimize today?",
        help: "I can help you with programming questions, explain the Pacman AI code, or give you advice on modern web aesthetics. Try clicking one of the suggested topics below!",
        default: "That's fascinating! Let's explore that further. If you have questions about the Pacman game code or Python optimization, feel free to ask!"
    };

    // Suggestions List
    const SUGGESTIONS = [
        "🎮 How does Pacman AI work?",
        "💡 Tell me a cool Python tip!",
        "🚀 What is this chatbot project?"
    ];

    // Helper: Safe DOM creation of SVG from string
    function createSVGElement(svgString) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(svgString, 'image/svg+xml');
        return doc.documentElement;
    }

    // Initialize layout SVGs securely
    document.getElementById("botAvatarHeader").appendChild(createSVGElement(SVG_BOT));
    document.getElementById("sendBtn").appendChild(createSVGElement(SVG_SEND));

    // Theme Management
    let currentTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", currentTheme);
    updateThemeToggleIcon();

    function updateThemeToggleIcon() {
        const btn = document.getElementById("themeToggle");
        btn.replaceChildren();
        if (currentTheme === "dark") {
            btn.appendChild(createSVGElement(SVG_SUN));
        } else {
            btn.appendChild(createSVGElement(SVG_MOON));
        }
    }

    function toggleTheme() {
        currentTheme = currentTheme === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", currentTheme);
        localStorage.setItem("theme", currentTheme);
        updateThemeToggleIcon();
    }

    // Populate suggestions
    const suggestionsContainer = document.getElementById("suggestionsContainer");
    SUGGESTIONS.forEach(text => {
        const chip = document.createElement("button");
        chip.className = "suggestion-chip";
        chip.textContent = text;
        chip.onclick = () => {
            document.getElementById("userInput").value = text;
            sendMessage();
        };
        suggestionsContainer.appendChild(chip);
    });

    // Append Message to UI safely
    function addMessage(text, sender) {
        const chatBox = document.getElementById("chatBox");
        
        const messageWrapper = document.createElement("div");
        messageWrapper.className = `message-wrapper ${sender}`;
        
        const avatar = document.createElement("div");
        avatar.className = "avatar";
        
        if (sender === "user") {
            avatar.appendChild(createSVGElement(SVG_USER));
        } else {
            avatar.appendChild(createSVGElement(SVG_BOT));
        }
        
        const bubble = document.createElement("div");
        bubble.className = "message-bubble";
        
        // SECURE: Use textContent to prevent XSS injection
        const textNode = document.createElement("span");
        textNode.textContent = text;
        bubble.appendChild(textNode);
        
        if (sender === "user") {
            messageWrapper.appendChild(bubble);
            messageWrapper.appendChild(avatar);
        } else {
            messageWrapper.appendChild(avatar);
            messageWrapper.appendChild(bubble);
        }
        
        chatBox.appendChild(messageWrapper);
        messageWrapper.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    // Typing Indicator management
    let typingIndicatorElement = null;

    function showTypingIndicator() {
        if (typingIndicatorElement) return;

        const chatBox = document.getElementById("chatBox");
        
        const wrapper = document.createElement("div");
        wrapper.className = "message-wrapper bot";
        
        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.appendChild(createSVGElement(SVG_BOT));
        
        const bubble = document.createElement("div");
        bubble.className = "message-bubble typing-indicator";
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement("div");
            dot.className = "typing-dot";
            bubble.appendChild(dot);
        }
        
        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);
        chatBox.appendChild(wrapper);
        
        typingIndicatorElement = wrapper;
        wrapper.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function removeTypingIndicator() {
        if (typingIndicatorElement && typingIndicatorElement.parentNode) {
            typingIndicatorElement.parentNode.removeChild(typingIndicatorElement);
        }
        typingIndicatorElement = null;
    }

    // Send Message Logic
    function sendMessage() {
        const input = document.getElementById("userInput");
        const text = input.value.trim();
        if (!text) return;

        // Append user message
        addMessage(text, "user");
        input.value = "";

        // Determine Response
        let response = BOT_RESPONSES.default;
        const normalized = text.toLowerCase();
        
        if (normalized.includes("pacman")) {
            response = BOT_RESPONSES.pacman;
        } else if (normalized.includes("python") || normalized.includes("code") || normalized.includes("optimize")) {
            response = BOT_RESPONSES.python;
        } else if (normalized.includes("project") || normalized.includes("chatbot") || normalized.includes("html")) {
            response = BOT_RESPONSES.project;
        } else if (normalized.includes("help")) {
            response = BOT_RESPONSES.help;
        } else if (normalized.includes("hello") || normalized.includes("hi")) {
            response = BOT_RESPONSES.hello;
        }

        // Show typing indicator, delay, then reply
        showTypingIndicator();
        setTimeout(() => {
            removeTypingIndicator();
            addMessage(response, "bot");
        }, 1000 + Math.random() * 800);
    }

    // Send on Enter
    document.getElementById("userInput").addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    // Greeting on load
    window.onload = () => {
        showTypingIndicator();
        setTimeout(() => {
            removeTypingIndicator();
            addMessage("Hello! I am Aether, your optimization assistant. How can I help you today?", "bot");
        }, 800);
    };
</script>

</body>
</html>
"""

class ChatbotHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            # Security Headers (Strictly enforced)
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('Content-Security-Policy', "default-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; script-src 'self' 'unsafe-inline';")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            self.send_error(404, "File not found")

    def log_message(self, format, *args):
        # Suppress normal logging of requests to keep stdout clean
        pass

def open_browser(url):
    # Short delay to guarantee the server is up and listening
    time.sleep(1.0)
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")

def main():
    PORT = 8000
    # Try successive ports if 8000 is occupied
    for offset in range(10):
        try:
            port = PORT + offset
            # Listen strictly on 127.0.0.1 (localhost) for security
            server_address = ('127.0.0.1', port)
            httpd = http.server.HTTPServer(server_address, ChatbotHandler)
            url = f"http://127.0.0.1:{port}/"
            
            print("==================================================")
            print(" AETHER AI CHATBOT SERVER")
            print("==================================================")
            print(f" Server running at: {url}")
            print(" Press Ctrl+C to stop the server.")
            print("==================================================")

            # Start browser launch in a background thread
            threading.Thread(target=open_browser, args=(url,), daemon=True).start()

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nStopping Aether AI Chatbot server...")
                httpd.server_close()
                sys.exit(0)
            break
        except OSError:
            # Port is occupied, try next one
            continue

if __name__ == '__main__':
    main()