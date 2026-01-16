import React, { useEffect, useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import {
    TrendingUp,
    TrendingDown,
    Layers,
    Activity,
    DollarSign,
    ShieldCheck,
    ArrowUpRight,
    Zap
} from 'lucide-react';
import { portfolioService } from '../services/api';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const StatCard = ({ label, value, change, icon: Icon, trend }) => (
    <div className="stat glass-card p-6 flex flex-col gap-2 transition-all hover:scale-[1.02]">
        <div className="flex justify-between items-start">
            <div className="p-3 bg-primary bg-opacity-10 rounded-xl text-primary border border-primary border-opacity-10">
                <Icon size={24} />
            </div>
            <div className={`badge ${trend === 'up' ? 'badge-success' : 'badge-error'} badge-sm font-bold gap-1`}>
                {trend === 'up' ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                {change}%
            </div>
        </div>
        <div className="mt-4">
            <div className="stat-title text-slate-500 font-bold text-xs uppercase tracking-widest">{label}</div>
            <div className="stat-value text-white text-3xl font-black mt-1">{value}</div>
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

    const chartData = {
        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '23:59'],
        datasets: [
            {
                label: 'Portfolio Value',
                data: [125000, 126500, 124000, 128000, 127000, 129500, 131000],
                fill: true,
                borderColor: '#0A84FF',
                backgroundColor: 'rgba(10, 132, 255, 0.1)',
                tension: 0.4,
                pointRadius: 0,
                borderWidth: 3,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: '#1c1c1e',
                titleColor: '#fff',
                bodyColor: '#fff',
                padding: 12,
                cornerRadius: 8,
                displayColors: false,
            },
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: { color: '#64748b', font: { size: 10, weight: 'bold' } },
            },
            y: {
                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                ticks: { color: '#64748b', font: { size: 10, weight: 'bold' }, callback: (value) => `$${value / 1000}k` },
            },
        },
    };

    if (loading) return (
        <div className="flex items-center justify-center h-[60vh]">
            <span className="loading loading-infinity loading-lg text-primary"></span>
        </div>
    );

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
            {/* Top Bar Analysis */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
                <div>
                    <h2 className="text-4xl font-black text-white elite-gradient-text tracking-tight">OPERATIONS_CENTER</h2>
                    <p className="text-slate-500 font-bold text-sm mt-2 flex items-center gap-2">
                        <Zap size={16} className="text-warning" />
                        SYSTEM_STATUS: <span className="text-success">OPTIMAL</span> // ENCRYPTION: <span className="text-info">AES-256</span>
                    </p>
                </div>
                <div className="flex gap-4">
                    <button className="btn btn-outline border-white border-opacity-10 text-white hover:bg-white hover:bg-opacity-5 rounded-xl font-bold uppercase text-xs tracking-widest px-8">
                        View Audit Log
                    </button>
                    <button className="btn btn-primary rounded-xl font-bold uppercase text-xs tracking-widest px-8 shadow-lg shadow-primary/20">
                        Optimize Assets
                    </button>
                </div>
            </div>

            {/* Matrix Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    label="Total Equity"
                    value={`$${(portfolio?.summary?.total_value || 131000.42).toLocaleString()}`}
                    change="+5.2"
                    icon={DollarSign}
                    trend="up"
                />
                <StatCard
                    label="Floating PnL"
                    value={`+$${(portfolio?.summary?.unrealized_pnl || 12450.00).toLocaleString()}`}
                    change="+12.4"
                    icon={Activity}
                    trend="up"
                />
                <StatCard
                    label="Active Nodes"
                    value={(portfolio?.positions?.length || 12).toString()}
                    change="0.0"
                    icon={Layers}
                    trend="up"
                />
                <StatCard
                    label="Risk Score"
                    value="0.14"
                    change="-2.1"
                    icon={ShieldCheck}
                    trend="down"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                {/* Main Visualizer */}
                <div className="lg:col-span-8 space-y-8">
                    <div className="glass-card p-8 h-[500px] flex flex-col">
                        <div className="flex justify-between items-center mb-10">
                            <div>
                                <h3 className="text-xl font-black text-white tracking-tight">EQUITY_STRATIFICATION</h3>
                                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">Real-time valuation synchronization</p>
                            </div>
                            <div className="join">
                                <button className="btn btn-sm join-item bg-white bg-opacity-5 border-white border-opacity-5">1H</button>
                                <button className="btn btn-sm join-item btn-primary">1D</button>
                                <button className="btn btn-sm join-item bg-white bg-opacity-5 border-white border-opacity-5">1W</button>
                            </div>
                        </div>
                        <div className="flex-1 min-h-0">
                            <Line data={chartData} options={chartOptions} />
                        </div>
                    </div>

                    {/* Positions Table */}
                    <div className="glass-card overflow-hidden">
                        <div className="p-8 border-b border-white border-opacity-5">
                            <h3 className="text-xl font-black text-white tracking-tight">ACTIVE_ALLOCATIONS</h3>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="table table-zebra bg-transparent">
                                <thead>
                                    <tr className="border-white border-opacity-5 text-slate-500 uppercase text-[10px] tracking-widest">
                                        <th className="pl-8 py-6">Asset_Identifier</th>
                                        <th>Size_Allocation</th>
                                        <th>Market_Value</th>
                                        <th>Variance_%</th>
                                        <th className="pr-8 text-right">Operational_Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {(portfolio?.positions || [
                                        { symbol: 'BTCUSDT', quantity: '1.24', market_value: 54120, pnl_percent: 5.8, share: 45 },
                                        { symbol: 'ETHUSDT', quantity: '18.5', market_value: 42100, pnl_percent: -2.3, share: 35 },
                                        { symbol: 'SOLUSDT', quantity: '245', market_value: 12400, pnl_percent: 1.2, share: 20 }
                                    ]).map((pos, i) => (
                                        <tr key={i} className="hover:bg-white hover:bg-opacity-5 border-white border-opacity-5 transition-colors group">
                                            <td className="pl-8 py-5">
                                                <div className="flex items-center gap-4">
                                                    <div className="w-10 h-10 rounded-xl bg-primary bg-opacity-10 flex items-center justify-center font-bold text-primary border border-primary border-opacity-20 group-hover:scale-110 transition-transform">
                                                        {pos.symbol.substring(0, 2)}
                                                    </div>
                                                    <div>
                                                        <p className="font-bold text-white text-sm tracking-wide">{pos.symbol}</p>
                                                        <p className="text-[10px] font-bold text-slate-500 uppercase">Layer-1 Protocol</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="font-bold text-slate-300 text-sm">{pos.quantity} units</td>
                                            <td className="font-bold text-white text-sm">${pos.market_value?.toLocaleString()}</td>
                                            <td>
                                                <div className={`badge ${pos.pnl_percent >= 0 ? 'badge-success' : 'badge-error'} badge-sm font-bold bg-opacity-20 border-opacity-30`}>
                                                    {pos.pnl_percent >= 0 ? '+' : ''}{pos.pnl_percent}%
                                                </div>
                                            </td>
                                            <td className="pr-8 text-right">
                                                <button className="btn btn-ghost btn-xs text-primary font-bold hover:bg-primary hover:bg-opacity-10 rounded-lg h-10 px-4">
                                                    MANAGE_ENTRY <ArrowUpRight size={14} className="ml-1" />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Intelligent Insights */}
                <div className="lg:col-span-4 space-y-8">
                    <div className="glass-card p-8 bg-primary bg-opacity-10 border-primary border-opacity-20 shadow-primary/5">
                        <h3 className="text-xl font-black text-white tracking-tight mb-4">AI_INSIGHTS_v1.0</h3>
                        <p className="text-slate-400 text-sm font-medium leading-relaxed mb-8">
                            Market volatility is currently <span className="text-success font-bold text-white">LOW</span>.
                            Alpha monitoring suggests increasing capital allocation in <span className="underline decoration-primary font-bold text-white">TECH-INDEX</span> assets for the next 4 hours.
                        </p>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center bg-white bg-opacity-5 p-4 rounded-xl border border-white border-opacity-5">
                                <span className="text-xs font-bold text-slate-300">Confidence Score</span>
                                <span className="text-xs font-black text-primary">89.4%</span>
                            </div>
                            <button className="btn btn-primary w-full h-14 rounded-2xl font-black uppercase text-xs tracking-widest">
                                Approve Strategy
                            </button>
                        </div>
                    </div>

                    <div className="glass-card">
                        <div className="p-8 border-b border-white border-opacity-5 flex justify-between items-center">
                            <h3 className="text-sm font-black text-slate-500 uppercase tracking-[0.2em]">Operational_Node_Vitals</h3>
                            <div className="w-2 h-2 rounded-full bg-success animate-ping" />
                        </div>
                        <div className="p-8 space-y-6">
                            {[
                                { label: 'Backend Latency', value: '14ms', progress: 15 },
                                { label: 'Node CPU Load', value: '32%', progress: 32 },
                                { label: 'Redis Buffer', value: '12%', progress: 12 },
                                { label: 'Socket Stream', value: '4.2kb/s', progress: 45 },
                            ].map((v, i) => (
                                <div key={i} className="space-y-3">
                                    <div className="flex justify-between items-end">
                                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{v.label}</span>
                                        <span className="text-xs font-bold text-white">{v.value}</span>
                                    </div>
                                    <progress className="progress progress-primary w-full bg-white bg-opacity-5 h-1.5" value={v.progress} max="100"></progress>
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
