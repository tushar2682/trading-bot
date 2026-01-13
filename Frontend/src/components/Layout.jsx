import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, BarChart3, Workflow, LogOut, Search, Bell, User, ChevronRight, Globe, ShieldCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Sidebar = () => {
    const navItems = [
        { icon: LayoutDashboard, label: 'Analytics Dashboard', path: '/' },
        { icon: BarChart3, label: 'Market Execution', path: '/trading' },
        { icon: Workflow, label: 'Automation Flows', path: '/workflows' },
    ];

    return (
        <div className="w-[280px] h-screen sticky top-0 bg-[#0f172a] flex flex-col pt-10 text-slate-300 border-r border-slate-800 shadow-2xl">
            {/* Business Branding */}
            <div className="px-8 mb-12 flex items-center gap-3">
                <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
                    <Globe className="text-white" size={20} />
                </div>
                <div>
                    <span className="text-xl font-bold tracking-tight text-white block leading-none">NEBU-CORP</span>
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">Trading Terminal</span>
                </div>
            </div>

            {/* Primary Navigation */}
            <nav className="flex-1 px-4 space-y-1">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `sidebar-link ${isActive ? 'active' : ''}`
                        }
                    >
                        <item.icon size={20} />
                        <span className="text-[14px] font-semibold">{item.label}</span>
                    </NavLink>
                ))}
            </nav>

            {/* Account / Operational Status */}
            <div className="p-6 border-t border-slate-800/50">
                <div className="mb-6 p-4 rounded-xl bg-slate-900/50 border border-slate-800 group cursor-pointer hover:border-slate-700 transition-all">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-xs font-bold text-blue-400 border border-slate-700">
                            JD
                        </div>
                        <div className="flex-1 overflow-hidden">
                            <p className="text-xs font-bold text-white truncate">John Doe</p>
                            <p className="text-[10px] text-slate-500 font-bold uppercase truncate">Senior Operator</p>
                        </div>
                        <ChevronRight size={14} className="text-slate-600 group-hover:text-slate-400" />
                    </div>
                    <div className="flex items-center gap-1.5 text-[10px] font-bold text-emerald-500">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
                        SYSTEM ENCRYPTED
                    </div>
                </div>

                <button
                    onClick={() => {
                        localStorage.removeItem('token');
                        window.location.href = '/login';
                    }}
                    className="w-full flex items-center gap-3 px-4 py-3 text-slate-500 hover:text-white hover:bg-slate-800/50 rounded-lg transition-all font-bold text-xs uppercase tracking-wider"
                >
                    <LogOut size={16} />
                    Sign Out Terminal
                </button>
            </div>
        </div>
    );
};

const Header = () => {
    return (
        <header className="h-20 bg-white border-b border-slate-200 sticky top-0 z-30 px-10 flex items-center justify-between shadow-sm">
            <div className="flex items-center gap-10 flex-1">
                <div className="max-w-md w-full relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                        type="text"
                        placeholder="Search assets, strategies, or transaction logs..."
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl py-3 pl-12 pr-4 text-sm outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500/50 transition-all font-medium text-slate-700"
                    />
                </div>

                <div className="hidden xl:flex items-center gap-6">
                    <div className="flex items-center gap-2">
                        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Global Status</span>
                        <span className="px-2 py-0.5 bg-blue-50 text-blue-600 text-[10px] font-black rounded uppercase">Operational</span>
                    </div>
                    <div className="w-px h-6 bg-slate-200" />
                    <div className="flex items-center gap-2">
                        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Market</span>
                        <span className="text-[11px] font-bold text-emerald-600 uppercase">Synchronized</span>
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-5">
                <div className="flex items-center gap-1 p-1 bg-slate-50 border border-slate-200 rounded-xl">
                    <button className="p-2 text-slate-500 hover:text-blue-600 hover:bg-white rounded-lg transition-all" title="Notifications">
                        <Bell size={20} />
                    </button>
                    <button className="p-2 text-slate-500 hover:text-blue-600 hover:bg-white rounded-lg transition-all" title="Security Settings">
                        <ShieldCheck size={20} />
                    </button>
                </div>

                <button className="btn-biz btn-biz-primary px-8 h-[48px] shadow-lg shadow-blue-500/10">
                    Executive Summary
                </button>
            </div>
        </header>
    );
};

export { Sidebar, Header };
