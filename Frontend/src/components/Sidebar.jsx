import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, TrendingUp, Cpu, LogOut, ChevronLeft, Menu } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Sidebar = () => {
    const [collapsed, setCollapsed] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);

    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
        { icon: TrendingUp, label: 'Execution', path: '/trading' },
        { icon: Cpu, label: 'Automations', path: '/workflows' },
    ];

    const SidebarContent = () => (
        <div className={`h-full flex flex-col p-4 transition-all duration-300 ${collapsed ? 'w-20' : 'w-72'} glass border-r border-white/5`}>
            {/* Brand */}
            <div className="flex items-center gap-4 mb-10 px-2 mt-4">
                <div className="min-w-[40px] h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
                    <TrendingUp className="text-white" size={24} />
                </div>
                {!collapsed && (
                    <motion.h1
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-xl font-bold tracking-tighter bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent truncate"
                    >
                        NEBU-TERMINAL
                    </motion.h1>
                )}
            </div>

            {/* Nav */}
            <nav className="flex-1 space-y-1">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center gap-4 px-3 py-3 rounded-xl transition-all group ${isActive
                                ? 'bg-indigo-600/10 text-indigo-400 shadow-[inset_0_0_0_1px_rgba(99,102,241,0.2)]'
                                : 'text-slate-400 hover:bg-white/5 hover:text-white'
                            }`
                        }
                    >
                        <item.icon size={20} className="min-w-[20px]" />
                        {!collapsed && <span className="font-medium whitespace-nowrap">{item.label}</span>}
                    </NavLink>
                ))}
            </nav>

            {/* Footer */}
            <div className="mt-auto space-y-2 border-t border-white/5 pt-6">
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="hidden lg:flex items-center gap-4 px-3 py-3 w-full text-slate-400 hover:bg-white/5 rounded-xl transition-all"
                >
                    <ChevronLeft className={`transition-transform duration-300 ${collapsed ? 'rotate-180' : ''}`} size={20} />
                    {!collapsed && <span className="font-medium">Collapse</span>}
                </button>

                <button
                    onClick={() => {
                        localStorage.removeItem('token');
                        window.location.href = '/login';
                    }}
                    className="flex items-center gap-4 px-3 py-3 w-full text-slate-400 hover:text-red-400 hover:bg-red-400/5 rounded-xl transition-all"
                >
                    <LogOut size={20} />
                    {!collapsed && <span className="font-medium">Logout</span>}
                </button>
            </div>
        </div>
    );

    return (
        <>
            {/* Mobile Toggle */}
            <button
                onClick={() => setMobileOpen(true)}
                className="lg:hidden fixed bottom-6 right-6 w-14 h-14 bg-indigo-600 rounded-full flex items-center justify-center text-white shadow-2xl z-50"
            >
                <Menu size={24} />
            </button>

            {/* Desktop Sidebar */}
            <div className="hidden lg:block h-screen sticky top-0">
                <SidebarContent />
            </div>

            {/* Mobile Overlay */}
            <AnimatePresence>
                {mobileOpen && (
                    <div className="fixed inset-0 z-[60] lg:hidden">
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setMobileOpen(false)}
                            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                        />
                        <motion.div
                            initial={{ x: '-100%' }}
                            animate={{ x: 0 }}
                            exit={{ x: '-100%' }}
                            className="absolute inset-y-0 left-0"
                        >
                            <SidebarContent />
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </>
    );
};

export default Sidebar;
