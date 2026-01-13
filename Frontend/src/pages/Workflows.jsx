import React, { useState, useEffect } from 'react';
import { workflowService } from '../services/api';
import { Play, Plus, Cpu, ShieldCheck, Activity, Terminal, ExternalLink, Settings2, MoreVertical, Database } from 'lucide-react';
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
            alert("Operational Fault: Protocol Change Denied");
        }
    };

    const executeWorkflow = async (id) => {
        try {
            await workflowService.executeWorkflow(id);
            alert("Tactical override successful.");
        } catch (err) {
            alert("Execution Error: Core Node Unresponsive");
        }
    };

    return (
        <div className="animate-biz max-w-[1600px] mx-auto space-y-8 pb-10">
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                <div>
                    <div className="flex items-center gap-2 mb-2">
                        <Cpu className="text-blue-600" size={16} />
                        <span className="text-[11px] font-bold uppercase tracking-[0.15em] text-slate-400">Tactical Automation Controller</span>
                    </div>
                    <h1 className="text-3xl font-bold text-slate-900 font-heading">Strategy Orchestration</h1>
                    <p className="text-slate-500 font-medium mt-1">Manage and monitor high-frequency autonomous trading protocols.</p>
                </div>
                <button className="btn-biz btn-biz-primary px-8 h-12 shadow-blue-500/10">
                    <Plus size={18} />
                    Create Protocol
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {workflows.map((wf) => (
                    <div key={wf.id} className="biz-card flex flex-col group p-0 overflow-hidden">
                        <div className="p-6 pb-0 flex justify-between items-start mb-6">
                            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all bg-opacity-10 ${wf.is_active ? 'bg-emerald-500 text-emerald-600' : 'bg-slate-200 text-slate-400'
                                }`}>
                                <Activity size={28} />
                            </div>
                            <div className="flex items-center gap-2">
                                <button className="p-2 text-slate-300 hover:text-slate-600 hover:bg-slate-50 rounded-lg transition-all"><Settings2 size={18} /></button>
                                <button className="p-2 text-slate-300 hover:text-slate-600 hover:bg-slate-50 rounded-lg transition-all"><MoreVertical size={18} /></button>
                            </div>
                        </div>

                        <div className="px-6 flex-1">
                            <h3 className="text-lg font-bold mb-2 text-slate-900 group-hover:text-blue-600 transition-colors uppercase tracking-tight">{wf.name}</h3>
                            <p className="text-xs text-slate-500 font-medium mb-6 leading-relaxed">
                                {wf.description || "Automatic monitoring and autonomous execution strategy using L1 liquidity signals and order-flow imbalances."}
                            </p>

                            <div className="grid grid-cols-2 gap-4 mb-8">
                                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Last Deploy</p>
                                    <p className="text-[11px] font-bold text-slate-700">6h 12m ago</p>
                                </div>
                                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Latency</p>
                                    <p className="text-[11px] font-bold text-blue-600">Adaptive (4ms)</p>
                                </div>
                            </div>
                        </div>

                        <div className="px-6 py-6 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
                            <div className="flex gap-3">
                                <button
                                    onClick={() => executeWorkflow(wf.id)}
                                    className="px-4 py-2.5 bg-white text-slate-600 border border-slate-200 rounded-xl hover:bg-blue-600 hover:text-white hover:border-blue-600 transition-all shadow-sm font-bold text-xs flex items-center gap-2"
                                >
                                    <Play size={14} fill="currentColor" />
                                    Manual Burst
                                </button>
                                <button
                                    onClick={() => toggleWorkflow(wf.id)}
                                    className={`px-5 py-2.5 rounded-xl font-bold text-xs uppercase tracking-widest transition-all ${wf.is_active
                                            ? 'bg-rose-50 text-rose-600 hover:bg-rose-600 hover:text-white border border-rose-100'
                                            : 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/10'
                                        }`}
                                >
                                    {wf.is_active ? 'Shut Down' : 'Establish'}
                                </button>
                            </div>
                            <div className={`flex items-center gap-2 text-[10px] font-black tracking-widest ${wf.is_active ? 'text-emerald-600' : 'text-slate-300'}`}>
                                <div className={`w-1.5 h-1.5 rounded-full ${wf.is_active ? 'bg-emerald-500 animate-pulse' : 'bg-slate-300'}`} />
                                {wf.is_active ? 'ONLINE' : 'IDLE'}
                            </div>
                        </div>
                    </div>
                ))}

                {!loading && workflows.length === 0 && (
                    <div className="col-span-full py-40 biz-card border-dashed bg-transparent shadow-none flex flex-col items-center justify-center text-slate-300">
                        <Database size={48} strokeWidth={1} className="mb-6 opacity-40" />
                        <p className="text-sm font-bold uppercase tracking-[0.2em]">No Automation Protocols Identified</p>
                        <button className="mt-8 px-6 py-3 bg-white border border-slate-200 text-slate-500 font-bold text-xs rounded-xl hover:bg-slate-50 transition-all flex items-center gap-2">
                            Access n8n Cloud <ExternalLink size={14} />
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Workflows;
