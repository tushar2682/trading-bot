import React, { useState, useEffect } from 'react';
import { workflowService } from '../services/api';
import {
    Play,
    Plus,
    Cpu,
    ShieldCheck,
    Activity,
    Terminal,
    ExternalLink,
    Settings2,
    MoreVertical,
    Database,
    Power,
    Zap,
    RefreshCw
} from 'lucide-react';
import { motion } from 'framer-motion';

const Workflows = () => {
    const [workflows, setWorkflows] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchWorkflows();
    }, []);

    const fetchWorkflows = async () => {
        try {
            const res = await workflowService.getWorkflows();
            setWorkflows(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const toggleWorkflow = async (id) => {
        try {
            await workflowService.toggleWorkflow(id);
            fetchWorkflows();
        } catch (err) {
            console.error("Protocol shutdown failed", err);
        }
    };

    const executeWorkflow = async (id) => {
        try {
            await workflowService.executeWorkflow(id);
        } catch (err) {
            console.error("Execution failure", err);
        }
    };

    if (loading) return (
        <div className="flex items-center justify-center h-[60vh]">
            <span className="loading loading-infinity loading-lg text-primary"></span>
        </div>
    );

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-1000 pb-10">
            {/* Automation Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-white border-opacity-5 pb-8">
                <div>
                    <h2 className="text-4xl font-black text-white tracking-tight elite-gradient-text">STRATEGY_ORCHESTRATOR</h2>
                    <p className="text-slate-500 font-bold text-sm mt-2 flex items-center gap-2">
                        <Cpu size={16} className="text-primary" />
                        ACTIVE_INSTANCES: <span className="text-success">{workflows.filter(w => w.is_active).length}</span> // ENGINE: <span className="text-info">N-8-N_CORE</span>
                    </p>
                </div>
                <button className="btn btn-primary px-10 rounded-2xl font-black uppercase text-xs tracking-[0.2em] shadow-lg shadow-primary/20 h-14">
                    <Plus size={18} className="mr-2" />
                    REGISTER_NEW_PROTOCOL
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
                {workflows.map((wf) => (
                    <div key={wf.id} className="glass-card flex flex-col group overflow-hidden border-opacity-10 hover:border-opacity-30 transition-all duration-500">
                        <div className="p-8 pb-4 flex justify-between items-start">
                            <div className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-500 border ${wf.is_active
                                    ? 'bg-success bg-opacity-10 text-success border-success border-opacity-20 shadow-[0_0_20px_rgba(48,209,88,0.1)]'
                                    : 'bg-neutral bg-opacity-40 text-slate-600 border-white border-opacity-5'
                                }`}>
                                <Activity size={32} className={wf.is_active ? 'animate-pulse' : ''} />
                            </div>
                            <div className="flex items-center gap-1">
                                <button className="btn btn-ghost btn-square btn-sm text-slate-500 hover:text-white transition-colors"><Settings2 size={16} /></button>
                                <button className="btn btn-ghost btn-square btn-sm text-slate-500 hover:text-white transition-colors"><MoreVertical size={16} /></button>
                            </div>
                        </div>

                        <div className="px-8 flex-1">
                            <h3 className="text-xl font-black mb-3 text-white tracking-tight group-hover:text-primary transition-colors duration-300 uppercase">
                                {wf.name}
                            </h3>
                            <p className="text-xs text-slate-500 font-bold mb-8 leading-relaxed tracking-wide">
                                {wf.description || "INSTITUTIONAL_STRATEGY: Monitoring L1 liquidity anomalies and executing autonomous delta-neutral hedging protocols."}
                            </p>

                            <div className="grid grid-cols-2 gap-4 mb-10">
                                <div className="p-4 bg-neutral bg-opacity-20 rounded-2xl border border-white border-opacity-5">
                                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Last_Execution</p>
                                    <p className="text-xs font-black text-white">0.42s AGO</p>
                                </div>
                                <div className="p-4 bg-neutral bg-opacity-20 rounded-2xl border border-white border-opacity-5">
                                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Latency_Avg</p>
                                    <p className="text-xs font-black text-primary">12.4ms</p>
                                </div>
                            </div>
                        </div>

                        <div className="px-8 py-8 bg-white bg-opacity-[0.02] border-t border-white border-opacity-5 flex items-center justify-between">
                            <div className="flex gap-3">
                                <button
                                    onClick={() => executeWorkflow(wf.id)}
                                    className="btn btn-sm btn-outline border-white border-opacity-10 text-white hover:bg-white hover:bg-opacity-5 rounded-xl font-bold text-[10px] tracking-widest px-4 h-10"
                                >
                                    <RefreshCw size={12} className="mr-1" />
                                    SYNC_FORCE
                                </button>
                                <button
                                    onClick={() => toggleWorkflow(wf.id)}
                                    className={`btn btn-sm rounded-xl font-black text-[10px] tracking-[0.15em] px-6 h-10 transition-all duration-300 ${wf.is_active
                                            ? 'bg-error bg-opacity-10 text-error border-error border-opacity-20 hover:bg-error hover:text-white'
                                            : 'bg-primary text-white border-none shadow-lg shadow-primary/20'
                                        }`}
                                >
                                    {wf.is_active ? 'SHUTDOWN' : 'ESTABLISH'}
                                </button>
                            </div>
                            <div className={`flex items-center gap-2 text-[9px] font-black tracking-[0.2em] px-3 py-1.5 rounded-full border ${wf.is_active
                                    ? 'text-success border-success border-opacity-20 bg-success bg-opacity-5'
                                    : 'text-slate-500 border-white border-opacity-5 bg-neutral bg-opacity-20'
                                }`}>
                                <div className={`w-1.5 h-1.5 rounded-full ${wf.is_active ? 'bg-success animate-ping' : 'bg-slate-700'}`} />
                                {wf.is_active ? 'ONLINE' : 'STBY'}
                            </div>
                        </div>
                    </div>
                ))}

                {workflows.length === 0 && (
                    <div className="col-span-full py-48 glass-card border-dashed border-opacity-20 flex flex-col items-center justify-center text-slate-500">
                        <Database size={64} strokeWidth={0.5} className="mb-8 opacity-20" />
                        <p className="text-xs font-black uppercase tracking-[0.4em]">NO_INSTANTIATED_PROTOCOLS_FOUND</p>
                        <button className="mt-10 btn btn-outline border-white border-opacity-10 text-slate-400 hover:text-white rounded-2xl px-10 font-bold text-xs flex items-center gap-2">
                            ACCESS_REMOTE_CLOUD <ExternalLink size={16} />
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Workflows;
