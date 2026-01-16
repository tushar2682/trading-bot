import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import {
    LayoutDashboard,
    BarChart3,
    Workflow,
    LogOut,
    Search,
    Bell,
    User,
    Menu,
    Settings,
    Cpu,
    Globe
} from 'lucide-react';

const SidebarLink = ({ to, icon: Icon, label }) => (
    <NavLink
        to={to}
        className={({ isActive }) => `nav-link-elite ${isActive ? 'active' : ''}`}
    >
        <Icon size={20} />
        <span className="tracking-wide">{label}</span>
    </NavLink>
);

const Sidebar = () => {
    return (
        <div className="flex flex-col h-full glass-sidebar p-6 pt-10">
            {/* Brand */}
            <div className="flex items-center gap-4 px-4 mb-12">
                <div className="w-10 h-10 bg-primary bg-opacity-20 rounded-xl flex items-center justify-center border border-primary border-opacity-30 shadow-lg shadow-primary/20">
                    <Cpu className="text-primary" size={24} />
                </div>
                <div>
                    <h1 className="text-xl font-bold text-white tracking-tight leading-none">NEBU-TRADER</h1>
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mt-1">Command Terminal</p>
                </div>
            </div>

            {/* Navigation */}
            <div className="flex-1 space-y-2">
                <div className="px-4 mb-4">
                    <span className="text-[11px] font-bold text-slate-600 uppercase tracking-widest">Main Modules</span>
                </div>
                <SidebarLink to="/" icon={LayoutDashboard} label="Operations Center" />
                <SidebarLink to="/trading" icon={BarChart3} label="Market Execution" />
                <SidebarLink to="/workflows" icon={Workflow} label="Task Automation" />

                <div className="px-4 mt-10 mb-4">
                    <span className="text-[11px] font-bold text-slate-600 uppercase tracking-widest">Operational Secure</span>
                </div>
                <SidebarLink to="/settings" icon={Settings} label="System Config" />
            </div>

            {/* Bottom Profile */}
            <div className="mt-auto pt-6 border-t border-white border-opacity-5">
                <div className="flex items-center gap-4 p-4 rounded-2xl bg-white bg-opacity-5 border border-white border-opacity-5 hover:bg-opacity-10 transition-all cursor-pointer group">
                    <div className="avatar placeholder">
                        <div className="bg-neutral text-neutral-content rounded-full w-10">
                            <span className="text-xs">OP</span>
                        </div>
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-bold text-white truncate">OPERATOR_01</p>
                        <p className="text-[10px] font-bold text-success uppercase">Active Service</p>
                    </div>
                </div>

                <button
                    onClick={() => {
                        localStorage.removeItem('token');
                        window.location.href = '/login';
                    }}
                    className="w-full mt-4 flex items-center gap-3 px-6 py-4 text-slate-500 hover:text-white transition-all font-bold text-xs uppercase tracking-widest"
                >
                    <LogOut size={16} />
                    Disconnect
                </button>
            </div>
        </div>
    );
};

const Header = () => {
    return (
        <div className="navbar glass-card border-none rounded-none px-8 py-4 mb-8 sticky top-0 z-50">
            <div className="flex-none lg:hidden">
                <label htmlFor="my-drawer-2" className="btn btn-square btn-ghost drawer-button">
                    <Menu size={24} />
                </label>
            </div>

            <div className="flex-1 gap-8">
                <div className="form-control max-w-md w-full relative hidden md:block">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                    <input
                        type="text"
                        placeholder="Search terminal logs, assets, or scripts..."
                        className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary focus:border-opacity-30 pl-12 h-12 rounded-xl text-sm"
                    />
                </div>

                <div className="hidden xl:flex items-center gap-6 ml-4">
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-[0.1em]">Network Sync: 100%</span>
                    </div>
                    <div className="w-[1px] h-4 bg-white opacity-10" />
                    <div className="flex items-center gap-2">
                        <Globe size={14} className="text-primary" />
                        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-[0.1em]">Node: US-EAST-01</span>
                    </div>
                </div>
            </div>

            <div className="flex-none gap-4">
                <div className="indicator">
                    <span className="indicator-item badge badge-primary badge-xs"></span>
                    <button className="btn btn-ghost btn-circle text-slate-400 hover:text-primary transition-colors">
                        <Bell size={20} />
                    </button>
                </div>
                <button className="btn btn-ghost btn-circle text-slate-400 hover:text-primary transition-colors">
                    <User size={20} />
                </button>

                <div className="ml-2">
                    <button className="btn btn-primary px-8 rounded-xl font-bold text-xs uppercase tracking-widest shadow-lg shadow-primary/20 hover:scale-105 transition-all">
                        Execute Plan
                    </button>
                </div>
            </div>
        </div>
    );
};

const Layout = () => {
    return (
        <div className="drawer lg:drawer-open font-sans text-slate-300">
            <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />

            <div className="drawer-content flex flex-col min-h-screen bg-transparent">
                {/* Main Header */}
                <Header />

                {/* Page Content */}
                <main className="flex-1 px-8 pb-12 overflow-x-hidden">
                    <Outlet />
                </main>
            </div>

            <div className="drawer-side z-50">
                <label htmlFor="my-drawer-2" aria-label="close sidebar" className="drawer-overlay"></label>
                <Sidebar />
            </div>
        </div>
    );
};

export default Layout;
