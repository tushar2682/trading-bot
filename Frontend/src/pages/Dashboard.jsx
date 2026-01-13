import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';
import { ArrowUpRight, ArrowDownRight, TrendingUp, Briefcase, Activity, Clock, ChevronRight, Layers, DollarSign } from 'lucide-react';
import { motion } from 'framer-motion';
import { portfolioService } from '../services/api';

const StatCard = ({ label, value, change, icon: Icon, color }) => (
    <div className="biz-card flex flex-col justify-between">
        <div className="flex justify-between items-start mb-4">
            <div className={`p-2.5 rounded-xl ${color} bg-opacity-10`}>
                <Icon size={20} className={color.replace('bg-', 'text-')} />
            </div>
            <div className={`flex items-center gap-1 text-xs font-bold ${change >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                {change >= 0 ? <TrendingUp size={14} /> : <ArrowDownRight size={14} />}
                {Math.abs(change)}%
            </div>
        </div>
        <div>
            <p className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">{label}</p>
            <p className="text-2xl font-bold text-slate-900">{value}</p>
        </div>
    </div>
);

const Dashboard = () => {
    const [portfolio, setPortfolio] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await portfolioService.getPortfolio();
                setPortfolio(res.data);
            } catch (err) {
                console.error("Fetch failed", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const performanceData = [
        { name: 'Jan', value: 4000 }, { name: 'Feb', value: 3000 }, { name: 'Mar', value: 5000 },
        { name: 'Apr', value: 4500 }, { name: 'May', value: 6000 }, { name: 'Jun', value: 5500 },
        { name: 'Jul', value: 7000 }, { name: 'Aug', value: 6800 }, { name: 'Sep', value: 8500 },
    ];

    if (loading) return (
        <div className="flex items-center justify-center h-[60vh]">
            <div className="w-8 h-8 border-2 border-blue-500/20 border-t-blue-600 rounded-full animate-spin"></div>
        </div>
    );

    return (
        <div className="animate-biz max-w-[1600px] mx-auto space-y-8 pb-10">
            {/* Header Info */}
            <div className="flex items-end justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Analytics Overview</h1>
                    <p className="text-slate-500 font-medium mt-1">Institutional-grade portfolio performance tracking.</p>
                </div>
                <div className="flex items-center gap-3">
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">LATEST_REPORT: 6:30 AM EST</span>
                    <button className="btn-biz btn-biz-secondary">Export Analytics</button>
                </div>
            </div>

            {/* KPI Matrix */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard label="Total Equity Value" value={`$${(portfolio?.summary?.total_value || 128450.20).toLocaleString()}`} change={4.2} icon={DollarSign} color="bg-blue-500" />
                <StatCard label="Net PnL (Open)" value={`+$${(portfolio?.summary?.unrealized_pnl || 12450.00).toLocaleString()}`} change={12.5} icon={TrendingUp} color="bg-emerald-500" />
                <StatCard label="Active Allocations" value={(portfolio?.positions?.length || 18).toString()} change={0} icon={Layers} color="bg-slate-500" />
                <StatCard label="Execution Efficiency" value="98.4%" change={-1.2} icon={Activity} color="bg-indigo-500" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                {/* Main Performance Chart */}
                <div className="lg:col-span-8 space-y-8">
                    <div className="biz-card">
                        <div className="flex items-center justify-between mb-8">
                            <h3 className="text-lg font-bold">Equity Evolution</h3>
                            <div className="flex bg-slate-100 p-1 rounded-lg">
                                {['Total Portfolio', 'Sub-Engines'].map(t => (
                                    <button key={t} className={`px-4 py-1.5 text-[11px] font-bold rounded-md transition-all ${t === 'Total Portfolio' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500'}`}>
                                        {t}
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div className="h-[400px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={performanceData}>
                                    <defs>
                                        <linearGradient id="blueGrad" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#2563eb" stopOpacity={0.1} />
                                            <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} dy={10} />
                                    <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} dx={-10} tickFormatter={(v) => `$${v}`} />
                                    <Tooltip
                                        contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                                    />
                                    <Area
                                        type="monotone"
                                        dataKey="value"
                                        stroke="#2563eb"
                                        strokeWidth={3}
                                        fillOpacity={1}
                                        fill="url(#blueGrad)"
                                        animationDuration={1500}
                                    />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Asset Allocation Metrics */}
                    <div className="biz-card">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-lg font-bold">Asset Stratification</h3>
                            <button className="text-blue-600 font-bold text-xs hover:underline flex items-center gap-1">Update Protocol <ChevronRight size={14} /></button>
                        </div>
                        <div className="space-y-5">
                            {(portfolio?.positions || [
                                { symbol: 'BTCUSDT', quantity: '1.24', market_value: 54120, pnl_percent: 5.8, share: 45 },
                                { symbol: 'ETHUSDT', quantity: '18.5', market_value: 42100, pnl_percent: -2.3, share: 35 },
                                { symbol: 'SOLUSDT', quantity: '245', market_value: 12400, pnl_percent: 1.2, share: 20 }
                            ]).map((pos, i) => (
                                <div key={i} className="list-item rounded-xl">
                                    <div className="flex items-center gap-4 flex-1">
                                        <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center font-bold text-slate-500">
                                            {pos.symbol.substring(0, 2)}
                                        </div>
                                        <div>
                                            <p className="font-bold text-slate-900">{pos.symbol}</p>
                                            <p className="text-[11px] text-slate-400 font-bold uppercase tracking-tighter">{pos.quantity} UNITS ALLOCATED</p>
                                        </div>
                                    </div>
                                    <div className="flex-1 px-8">
                                        <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                                            <div className="h-full bg-blue-500 rounded-full" style={{ width: `${pos.share || 30}%` }} />
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <p className="font-bold text-slate-900">${pos.market_value?.toLocaleString()}</p>
                                        <p className={`text-[11px] font-bold ${pos.pnl_percent >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                                            {pos.pnl_percent >= 0 ? '+' : ''}{pos.pnl_percent}% VARIANCE
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Sidebar Business Intelligence */}
                <div className="lg:col-span-4 space-y-6">
                    <div className="biz-card bg-[#0f172a] text-white overflow-hidden relative border-none shadow-blue-900/10">
                        <div className="relative z-10">
                            <div className="flex items-center gap-2 mb-4">
                                <ShieldCheck className="text-blue-400" size={18} />
                                <span className="text-[10px] font-black uppercase tracking-widest text-blue-400">Secure Operation</span>
                            </div>
                            <h3 className="text-lg font-bold mb-2 font-heading">Alpha Monitoring</h3>
                            <p className="text-sm text-slate-400 font-medium leading-relaxed mb-8">System is autonomously validating 1,240 data points per second across global exchanges.</p>
                            <button className="w-full btn-biz btn-biz-primary h-12">Launch Terminal</button>
                        </div>
                        <Activity className="absolute -right-10 -bottom-10 text-white opacity-[0.03] scale-[3]" size={120} />
                    </div>

                    <div className="biz-card">
                        <h3 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-6 border-b border-slate-50 pb-4">Operational Status</h3>
                        <div className="space-y-4">
                            {[
                                { label: 'Latency (API)', value: '12ms', status: 'optimal' },
                                { label: 'DB Integrity', value: '100%', status: 'optimal' },
                                { label: 'n8n Node 01', value: 'Active', status: 'optimal' },
                                { label: 'Buffer Usage', value: '42%', status: 'warning' },
                            ].map((s, i) => (
                                <div key={i} className="flex justify-between items-center text-xs">
                                    <span className="text-slate-500 font-semibold">{s.label}</span>
                                    <div className="flex items-center gap-2">
                                        <span className="text-slate-900 font-bold">{s.value}</span>
                                        <div className={`w-1.5 h-1.5 rounded-full ${s.status === 'optimal' ? 'bg-emerald-500' : 'bg-amber-500'}`} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="biz-card p-0 overflow-hidden border-dashed">
                        <div className="p-6">
                            <h3 className="text-sm font-bold uppercase tracking-widest text-slate-500">Business Insights</h3>
                        </div>
                        <div className="p-2 space-y-1">
                            {['Market Sentimental Shift', 'Volume Anomaly Detected', 'Protocol v4.2 Update Ready'].map((msg, i) => (
                                <div key={i} className="p-4 rounded-xl hover:bg-slate-50 transition-all flex items-start gap-4 cursor-pointer">
                                    <div className="mt-1 w-2 h-2 rounded-full bg-blue-500" />
                                    <p className="text-xs font-bold text-slate-700 leading-tight">{msg}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
