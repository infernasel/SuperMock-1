"""
Command-line interface for SuperMock
"""

import argparse
import sys
import threading
from supermock.api import TelegramMockServer
from supermock.terminal import TerminalChat


def start_web(args):
    """Start the mock server with web UI"""
    from supermock.web import WebUIServer
    
    server = TelegramMockServer(host=args.host, port=args.port)
    
    # Start API server in background thread
    server_thread = threading.Thread(target=lambda: server.run(debug=False), daemon=True)
    server_thread.start()
    
    # Wait a bit for server to start
    import time
    time.sleep(1)
    
    # Start web UI
    web_server = WebUIServer(server, host=args.webhost, port=args.webport)
    
    try:
        web_server.run(debug=args.debug)
    except KeyboardInterrupt:
        print("\n\n👋 Stopping...")
    
    sys.exit(0)


def start_server(args):
    """Start the mock server only"""
    server = TelegramMockServer(host=args.host, port=args.port)
    
    try:
        server.run(debug=args.debug)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped.")
        sys.exit(0)


def start_interactive(args):
    """Start the mock server with interactive terminal chat"""
    server = TelegramMockServer(host=args.host, port=args.port)
    
    # Start server in background thread
    server_thread = threading.Thread(target=lambda: server.run(debug=False), daemon=True)
    server_thread.start()
    
    # Wait a bit for server to start
    import time
    time.sleep(1)
    
    # Start interactive chat
    chat = TerminalChat(server)
    
    try:
        chat.start_interactive()
    except KeyboardInterrupt:
        print("\n\n👋 Stopping...")
        chat.stop()
    
    sys.exit(0)


def main():
    """Main entry point for SuperMock CLI"""
    parser = argparse.ArgumentParser(
        description='SuperMock - Local Telegram Bot API Mock Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server only (for automated testing)
  supermock server
  
  # Start server on custom host/port
  supermock server --host 0.0.0.0 --port 8080
  
  # Start interactive terminal chat
  supermock chat
  
  # Start interactive chat on custom port
  supermock chat --port 8080
  
  # Start web-based UI
  supermock web
  
  # Start web UI on custom ports
  supermock web --port 8081 --webport 8082

For more information, visit: https://github.com/infernasel/SuperMock-1
        """
    )
    
    parser.add_argument('--version', action='version', version='SuperMock 0.2.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Start mock API server only')
    server_parser.add_argument('--host', type=str, default='localhost',
                              help='Host to bind the server to (default: localhost)')
    server_parser.add_argument('--port', type=int, default=8081,
                              help='Port to bind the server to (default: 8081)')
    server_parser.add_argument('--debug', action='store_true',
                              help='Enable debug mode')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Start interactive terminal chat')
    chat_parser.add_argument('--host', type=str, default='localhost',
                            help='Host to bind the server to (default: localhost)')
    chat_parser.add_argument('--port', type=int, default=8081,
                            help='Port to bind the server to (default: 8081)')
    
    # Web command
    web_parser = subparsers.add_parser('web', help='Start web-based UI')
    web_parser.add_argument('--host', type=str, default='localhost',
                           help='API server host (default: localhost)')
    web_parser.add_argument('--port', type=int, default=8081,
                           help='API server port (default: 8081)')
    web_parser.add_argument('--webhost', type=str, default='localhost',
                           help='Web UI host (default: localhost)')
    web_parser.add_argument('--webport', type=int, default=8082,
                           help='Web UI port (default: 8082)')
    web_parser.add_argument('--debug', action='store_true',
                           help='Enable debug mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'server':
        start_server(args)
    elif args.command == 'chat':
        start_interactive(args)
    elif args.command == 'web':
        start_web(args)


if __name__ == '__main__':
    main()
