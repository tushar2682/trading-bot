import React, { useState, useEffect } from 'react';
import { tradeService } from '../services/api';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Plus,
    BarChart3,
    Clock,
    ArrowRightLeft,
    ShieldCheck,
    Activity,
    Target,
    Zap,
    ChevronRight,
    ListFilter,
    ArrowUpRight,
    Send,
    Lock
} from 'lucide-react';

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
            console.error("Execution error", err);
        } finally {
            setExecuting(false);
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-1000 pb-10">
            {/* Terminal Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-white border-opacity-5 pb-8">
                <div>
                    <h2 className="text-4xl font-black text-white tracking-tight elite-gradient-text">EXECUTION_TERMINAL</h2>
                    <p className="text-slate-500 font-bold text-sm mt-2 flex items-center gap-2">
                        <Activity size={16} className="text-primary" />
                        DIRECT_MARKET_ACCESS: <span className="text-success">ACTIVE</span> // NODE: <span className="text-info">LOCAL-SYNC</span>
                    </p>
                </div>
                <div className="tabs tabs-boxed bg-neutral bg-opacity-30 border border-white border-opacity-5 p-1 rounded-xl">
                    <a className="tab tab-active bg-primary bg-opacity-10 text-primary font-bold text-xs">STANDARD_EXCHANGE</a>
                    <a className="tab text-slate-500 font-bold text-xs hover:text-slate-300">ALGORITHMIC_GATEWAY</a>
                </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-start">
                {/* Order Entry Node */}
                <div className="xl:col-span-4 space-y-6">
                    <div className="glass-card p-8 group">
                        <div className="flex items-center justify-between mb-8 pb-4 border-b border-white border-opacity-5">
                            <h3 className="text-sm font-black text-slate-500 uppercase tracking-[0.2em] flex items-center gap-2">
                                <Target size={18} className="text-primary group-hover:animate-pulse" />
                                DISPATCH_CENTER
                            </h3>
                            <div className="badge badge-success badge-outline badge-xs font-black p-2">LIVE</div>
                        </div>

                        <form className="space-y-6" onSubmit={handleCreateTrade}>
                            <div className="grid grid-cols-2 gap-2 p-1 bg-neutral bg-opacity-30 rounded-2xl border border-white border-opacity-5">
                                <button
                                    type="button"
                                    onClick={() => setFormData({ ...formData, side: 'buy' })}
                                    className={`py-3 rounded-xl text-xs font-black transition-all ${formData.side === 'buy' ? 'bg-success text-success-content shadow-lg shadow-success/20' : 'text-slate-500 hover:text-slate-300'}`}
                                >
                                    BUY_LONG
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setFormData({ ...formData, side: 'sell' })}
                                    className={`py-3 rounded-xl text-xs font-black transition-all ${formData.side === 'sell' ? 'bg-error text-error-content shadow-lg shadow-error/20' : 'text-slate-500 hover:text-slate-300'}`}
                                >
                                    SELL_SHORT
                                </button>
                            </div>

                            <div className="form-control w-full space-y-2">
                                <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Instrument_Ticker</label>
                                <input
                                    type="text"
                                    value={formData.symbol}
                                    onChange={(e) => setFormData({ ...formData, symbol: e.target.value.toUpperCase() })}
                                    className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary focus:ring-4 focus:ring-primary/5 font-black text-white rounded-xl placeholder:text-slate-700 h-14"
                                    placeholder="e.g. BTCUSDT"
                                    required
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="form-control w-full space-y-2">
                                    <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Size_Allocation</label>
                                    <input
                                        type="number"
                                        value={formData.quantity}
                                        onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                                        className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary font-black text-white rounded-xl h-14"
                                        placeholder="0.00"
                                        required
                                    />
                                </div>
                                <div className="form-control w-full space-y-2">
                                    <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Order_Protocol</label>
                                    <select
                                        value={formData.type}
                                        onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                                        className="select select-bordered w-full bg-neutral bg-opacity-40 border-white border-opacity-5 focus:border-primary font-black text-white rounded-xl h-14"
                                    >
                                        <option value="market">MARKET_IOC</option>
                                        <option value="limit">LIMIT_GTC</option>
                                    </select>
                                </div>
                            </div>

                            {formData.type === 'limit' && (
                                <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="form-control w-full space-y-2">
                                    <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Target_Execution_Price</label>
                                    <input
                                        type="number"
                                        value={formData.price}
                                        onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                                        className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary font-black text-white rounded-xl h-14"
                                        placeholder="0.00"
                                    />
                                </motion.div>
                            )}

                            <button
                                type="submit"
                                disabled={executing}
                                className={`btn btn-primary w-full h-16 rounded-2xl text-xs font-black uppercase tracking-[0.2em] shadow-lg shadow-primary/20 ${executing ? 'loading' : ''}`}
                            >
                                {executing ? 'STAGING_ORDER...' : `EXECUTE_${formData.side.toUpperCase()}_DISPATCH`}
                                {!executing && <Send size={16} className="ml-2" />}
                            </button>
                        </form>
                    </div>

                    <div className="glass-card p-6 bg-primary bg-opacity-5 border-primary border-opacity-20 flex items-start gap-4">
                        <div className="p-3 bg-primary bg-opacity-10 rounded-xl text-primary border border-primary border-opacity-20">
                            <Lock size={20} />
                        </div>
                        <div>
                            <p className="text-[10px] font-black text-primary uppercase tracking-widest mb-1">RISK_PROTOCOL_ACTIVE</p>
                            <p className="text-xs text-slate-400 font-medium leading-relaxed">
                                System slippage cap: <span className="text-white font-bold">0.5%</span>.
                                Automated stop-loss logic is standby for all manual executions.
                            </p>
                        </div>
                    </div>
                </div>

                {/* Secure Log Workspace */}
                <div className="xl:col-span-8">
                    <div className="glass-card min-h-[700px] flex flex-col overflow-hidden">
                        <div className="p-8 border-b border-white border-opacity-5 flex items-center justify-between bg-white bg-opacity-[0.02]">
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-2xl bg-primary bg-opacity-10 flex items-center justify-center border border-primary border-opacity-10">
                                    <Activity size={24} className="text-primary" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-black text-white tracking-tight">TRANSACTION_STREAM</h3>
                                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mt-1">Live ledger interaction</p>
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <button className="btn btn-ghost btn-square btn-sm text-slate-500 hover:text-primary transition-colors">
                                    <ListFilter size={18} />
                                </button>
                                <button className="btn btn-ghost btn-square btn-sm text-slate-500 hover:text-warning transition-colors">
                                    <Zap size={18} />
                                </button>
                            </div>
                        </div>

                        <div className="overflow-x-auto flex-1">
                            <table className="table table-zebra bg-transparent">
                                <thead>
                                    <tr className="border-white border-opacity-5 text-slate-500 uppercase text-[10px] tracking-widest">
                                        <th className="pl-10 py-6">Instrument_ID</th>
                                        <th>Direction</th>
                                        <th>Protocol</th>
                                        <th className="text-right">Quantity</th>
                                        <th className="text-right">Execution_Value</th>
                                        <th className="pr-10 text-center">Finalized_Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {trades.map((trade, i) => (
                                        <tr key={i} className="hover:bg-white hover:bg-opacity-5 border-white border-opacity-5 transition-colors group">
                                            <td className="pl-10 py-5">
                                                <div className="flex items-center gap-4">
                                                    <div className="w-9 h-9 rounded-xl bg-neutral bg-opacity-40 flex items-center justify-center font-bold text-xs text-slate-400 border border-white border-opacity-5">
                                                        {trade.symbol.substring(0, 2)}
                                                    </div>
                                                    <span className="font-black text-white text-sm tracking-wider">{trade.symbol}</span>
                                                </div>
                                            </td>
                                            <td>
                                                <div className={`badge ${trade.side === 'buy' ? 'badge-success' : 'badge-error'} badge-outline badge-xs font-black p-2 tracking-widest`}>
                                                    {trade.side.toUpperCase()}
                                                </div>
                                            </td>
                                            <td className="font-black text-[10px] text-slate-500 tracking-tighter uppercase">{trade.trade_type}</td>
                                            <td className="text-right font-black text-slate-300 text-sm">{trade.quantity}</td>
                                            <td className="text-right font-black text-white text-sm">${(trade.executed_price || trade.price || 0).toLocaleString()}</td>
                                            <td className="pr-10 text-center">
                                                <div className={`badge ${trade.status === 'filled' ? 'badge-primary' : 'badge-ghost'} bg-opacity-10 border-opacity-20 font-black text-[10px] py-3 px-4 tracking-widest`}>
                                                    {trade.status.toUpperCase()}
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                    {trades.length === 0 && (
                                        <tr>
                                            <td colSpan="6" className="py-48 text-center opacity-20">
                                                <div className="flex flex-col items-center gap-6">
                                                    <ArrowRightLeft size={64} strokeWidth={0.5} />
                                                    <p className="text-[11px] font-black uppercase tracking-[0.4em]">Zero_Chain_Interaction_Detected</p>
                                                </div>
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>

                        <div className="p-8 bg-white bg-opacity-[0.01] border-t border-white border-opacity-5 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                                <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">PERSISTENT_LEDGER_SYNC_OPTIMAL</p>
                            </div>
                            <button className="btn btn-link btn-xs text-primary font-black uppercase tracking-widest hover:no-underline flex items-center gap-2 p-0">
                                EXPORT_AUDIT_REPORT <ChevronRight size={14} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Trading;
