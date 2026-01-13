import React, { useState, useEffect } from 'react';
import { tradeService } from '../services/api';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, BarChart3, Clock, ArrowRightLeft, ShieldCheck, Activity, Target, Zap, ChevronRight, ListFilter } from 'lucide-react';

const Trading = () => {
    const [trades, setTrades] = useState([]);
    const [formData, setFormData] = useState({
        symbol: '',
        side: 'buy',
        type: 'market',
        quantity: '',
        price: ''
    });
    const [executing, setExecuting] = useState(false);

    useEffect(() => {
        fetchTrades();
    }, []);

    const fetchTrades = async () => {
        try {
            const res = await tradeService.getTrades();
            setTrades(res.data.trades);
        } catch (err) {
            console.error(err);
        }
    };

    const handleCreateTrade = async (e) => {
        e.preventDefault();
        setExecuting(true);
        try {
            await tradeService.createTrade(formData);
            fetchTrades();
            setFormData({ ...formData, symbol: '', quantity: '', price: '' });
        } catch (err) {
            alert("Execution Error: Order rejected by gateway.");
        } finally {
            setExecuting(false);
        }
    };

    return (
        <div className="animate-biz max-w-[1600px] mx-auto space-y-8 pb-10">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Execution Terminal</h1>
                    <p className="text-slate-500 font-medium mt-1">High-fidelity direct market access and order management.</p>
                </div>
                <div className="flex bg-slate-100 p-1 rounded-xl border border-slate-200">
                    <button className="px-5 py-2 text-xs font-bold bg-white text-blue-600 rounded-lg shadow-sm">Standard Order</button>
                    <button className="px-5 py-2 text-xs font-bold text-slate-500 hover:text-slate-700 rounded-lg transition-all">Algorithmic</button>
                </div>
            </header>

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-start">
                {/* Terminal Order Panel */}
                <div className="xl:col-span-4 space-y-6">
                    <div className="biz-card">
                        <div className="flex items-center justify-between mb-8 pb-4 border-b border-slate-50">
                            <h2 className="text-sm font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2">
                                <Target size={18} className="text-blue-500" />
                                Market Dispatch
                            </h2>
                            <div className="flex items-center gap-1.5">
                                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]" />
                                <span className="text-[10px] font-black text-emerald-600 uppercase tracking-tighter">Connected</span>
                            </div>
                        </div>

                        <form className="space-y-6" onSubmit={handleCreateTrade}>
                            <div className="grid grid-cols-2 gap-1 p-1 bg-slate-50 rounded-xl border border-slate-200/60">
                                <button
                                    type="button"
                                    onClick={() => setFormData({ ...formData, side: 'buy' })}
                                    className={`py-2.5 rounded-lg text-xs font-bold px-4 transition-all ${formData.side === 'buy' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/10' : 'text-slate-500 hover:text-slate-700'}`}
                                >
                                    BUY ASSET
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setFormData({ ...formData, side: 'sell' })}
                                    className={`py-2.5 rounded-lg text-xs font-bold px-4 transition-all ${formData.side === 'sell' ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/10' : 'text-slate-500 hover:text-slate-700'}`}
                                >
                                    SELL ASSET
                                </button>
                            </div>

                            <div className="space-y-2">
                                <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Instrument Symbol</label>
                                <input
                                    type="text"
                                    value={formData.symbol}
                                    onChange={(e) => setFormData({ ...formData, symbol: e.target.value.toUpperCase() })}
                                    className="w-full bg-slate-50 border border-slate-200 p-4 rounded-xl text-slate-900 outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500/50 font-bold text-sm tracking-tight transition-all"
                                    placeholder="e.g. BTCUSDT"
                                    required
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Order Size</label>
                                    <input
                                        type="number"
                                        value={formData.quantity}
                                        onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                                        className="w-full bg-slate-50 border border-slate-200 p-4 rounded-xl text-slate-900 outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500/50 font-bold text-sm transition-all"
                                        placeholder="0.00"
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Execution Mode</label>
                                    <select
                                        value={formData.type}
                                        onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                                        className="w-full bg-slate-50 border border-slate-200 p-4 rounded-xl text-slate-900 outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500/50 font-bold text-xs uppercase transition-all"
                                    >
                                        <option value="market">Market Price</option>
                                        <option value="limit">Limit Order</option>
                                    </select>
                                </div>
                            </div>

                            {formData.type === 'limit' && (
                                <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} className="space-y-2">
                                    <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Target Limit Price</label>
                                    <input
                                        type="number"
                                        value={formData.price}
                                        onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                                        className="w-full bg-slate-50 border border-slate-200 p-4 rounded-xl text-slate-900 outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500/50 font-bold text-sm transition-all"
                                        placeholder="0.00"
                                    />
                                </motion.div>
                            )}

                            <button
                                type="submit"
                                disabled={executing}
                                className={`w-full h-14 rounded-xl text-sm font-bold uppercase tracking-widest transition-all shadow-xl ${formData.side === 'buy' ? 'bg-emerald-600 text-white hover:bg-emerald-700 shadow-emerald-500/10' : 'bg-rose-600 text-white hover:bg-rose-700 shadow-rose-500/10'
                                    } ${executing && 'opacity-70 pointer-events-none'}`}
                            >
                                {executing ? 'Processing Order...' : `Place ${formData.side.toUpperCase()} Order`}
                            </button>
                        </form>
                    </div>

                    <div className="biz-card border-dashed bg-slate-50/50 flex items-start gap-4">
                        <div className="p-2 bg-blue-500/10 rounded-lg">
                            <ShieldCheck size={18} className="text-blue-600" />
                        </div>
                        <div>
                            <p className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">Risk Governance</p>
                            <p className="text-xs text-slate-500 font-medium leading-relaxed">System-wide slippage protection is active (0.5%). All orders are mapped to individual sub-accounts with full transparency.</p>
                        </div>
                    </div>
                </div>

                {/* Transaction History Workspace */}
                <div className="xl:col-span-8">
                    <div className="biz-card min-h-[600px] flex flex-col p-0 overflow-hidden">
                        <div className="p-6 border-b border-slate-100 flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <Activity size={20} className="text-blue-600" />
                                <h2 className="text-lg font-bold">Transaction History</h2>
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="flex bg-slate-50 border border-slate-200 p-1 rounded-lg">
                                    <button className="p-2 text-slate-400 hover:text-slate-600 transition-colors"><ListFilter size={16} /></button>
                                    <button className="p-2 text-slate-400 hover:text-slate-600 transition-colors"><Zap size={16} /></button>
                                </div>
                            </div>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="text-left text-[11px] font-bold uppercase tracking-widest text-slate-400 border-b border-slate-50">
                                        <th className="px-8 py-5">Instrument</th>
                                        <th className="px-8 py-5">Side</th>
                                        <th className="px-8 py-5">Mode</th>
                                        <th className="px-8 py-5 text-right">Quantity</th>
                                        <th className="px-8 py-5 text-right">Execution Price</th>
                                        <th className="px-8 py-5 text-center">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-50">
                                    {trades.map((trade, i) => (
                                        <tr key={i} className="list-item-row group hover:bg-slate-50/80 transition-all">
                                            <td className="px-8 py-5">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-8 h-8 rounded bg-slate-100 flex items-center justify-center font-bold text-[10px] text-slate-500">
                                                        {trade.symbol.substring(0, 2)}
                                                    </div>
                                                    <span className="font-bold text-slate-900">{trade.symbol}</span>
                                                </div>
                                            </td>
                                            <td className="px-8 py-5">
                                                <span className={`pill text-[10px] ${trade.side === 'buy' ? 'pill-up' : 'pill-down'}`}>
                                                    {trade.side}
                                                </span>
                                            </td>
                                            <td className="px-8 py-5 font-bold text-[11px] text-slate-500 uppercase">{trade.trade_type}</td>
                                            <td className="px-8 py-5 text-right font-bold text-slate-900">{trade.quantity}</td>
                                            <td className="px-8 py-5 text-right font-bold text-slate-900">${(trade.executed_price || trade.price || 0).toLocaleString()}</td>
                                            <td className="px-8 py-5 text-center">
                                                <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-tighter ${trade.status === 'filled' ? 'bg-blue-50 text-blue-600 border border-blue-100' : 'bg-slate-50 text-slate-400 border border-slate-100'
                                                    }`}>
                                                    {trade.status}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                    {trades.length === 0 && (
                                        <tr>
                                            <td colSpan="6" className="py-32 text-center">
                                                <div className="flex flex-col items-center gap-4 opacity-30">
                                                    <ArrowRightLeft size={48} strokeWidth={1} text-slate-400 />
                                                    <p className="text-xs font-bold uppercase tracking-[0.2em] text-slate-500">No Historical Records Found</p>
                                                </div>
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>

                        <div className="mt-auto p-6 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
                            <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">End of Stream — Real-time Connection Persistent</p>
                            <button className="text-blue-600 font-bold text-xs flex items-center gap-1 hover:underline">Download Audit Log <ChevronRight size={14} /></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Trading;
