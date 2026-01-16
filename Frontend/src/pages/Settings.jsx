import React from 'react';
import {
    Settings,
    Shield,
    Key,
    Bell,
    Globe,
    Database,
    Cpu,
    Lock,
    Eye,
    Zap,
    Save
} from 'lucide-react';

const SettingsCard = ({ title, description, icon: Icon, children }) => (
    <div className="glass-card p-8 border-opacity-10">
        <div className="flex items-start gap-6 mb-8">
            <div className="w-14 h-14 bg-primary bg-opacity-10 rounded-2xl flex items-center justify-center border border-primary border-opacity-20 shadow-lg shadow-primary/10">
                <Icon size={24} className="text-primary" />
            </div>
            <div>
                <h3 className="text-xl font-black text-white tracking-tight uppercase">{title}</h3>
                <p className="text-slate-500 font-bold text-xs mt-1 tracking-wide">{description}</p>
            </div>
        </div>
        <div className="space-y-6">
            {children}
        </div>
    </div>
);

const SettingItem = ({ label, description, children }) => (
    <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 py-6 border-t border-white border-opacity-5">
        <div className="flex-1">
            <p className="text-sm font-black text-slate-300 uppercase tracking-wide">{label}</p>
            <p className="text-xs font-bold text-slate-600 mt-1">{description}</p>
        </div>
        <div className="flex-none">
            {children}
        </div>
    </div>
);

const SettingsPage = () => {
    return (
        <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-1000 pb-20">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-white border-opacity-5 pb-8">
                <div>
                    <h2 className="text-4xl font-black text-white tracking-tight elite-gradient-text">SYSTEM_CONFIGURATION</h2>
                    <p className="text-slate-500 font-bold text-sm mt-2 flex items-center gap-2 uppercase tracking-widest">
                        <Settings size={16} className="text-primary" />
                        CORE_ENGINE_v4.5.0 // SECURITY_LEVEL: <span className="text-success">ULTRA</span>
                    </p>
                </div>
                <button className="btn btn-primary px-10 rounded-2xl font-black uppercase text-xs tracking-[0.2em] shadow-lg shadow-primary/20 h-14">
                    <Save size={18} className="mr-2" />
                    COMMIT_CHANGES
                </button>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-10">
                {/* Security Configuration */}
                <SettingsCard
                    title="SECURITY_ENFORCEMENT"
                    description="Configure encryption protocols and authentication gateways."
                    icon={Shield}
                >
                    <SettingItem
                        label="Two-Factor Authentication"
                        description="Require hardware token or OTP for high-value executions."
                    >
                        <input type="checkbox" className="toggle toggle-primary" defaultChecked />
                    </SettingItem>
                    <SettingItem
                        label="Session Persistence"
                        description="Auto-disconnect terminal after inactivity period."
                    >
                        <select className="select select-bordered bg-neutral bg-opacity-30 border-white border-opacity-5 font-bold text-xs">
                            <option>15 MINUTES</option>
                            <option>1 HOUR</option>
                            <option>4 HOURS</option>
                            <option>NEVER</option>
                        </select>
                    </SettingItem>
                    <SettingItem
                        label="IP Whitelisting"
                        description="Restrict command access to approved network nodes."
                    >
                        <button className="btn btn-sm btn-outline border-white border-opacity-10 text-xs font-black tracking-widest px-4 h-10">MANAGE_NODES</button>
                    </SettingItem>
                </SettingsCard>

                {/* API & Connectivity */}
                <SettingsCard
                    title="API_CONNECTOR_HUB"
                    description="Sync institutional exchange keys and liquidity providers."
                    icon={Key}
                >
                    <SettingItem
                        label="Exchange Master Key"
                        description="Primary bridge to global liquidity pools."
                    >
                        <div className="flex gap-2">
                            <input type="password" value="************************" readOnly className="input input-sm bg-neutral bg-opacity-30 border-white border-opacity-5 font-bold text-xs" />
                            <button className="btn btn-sm btn-ghost btn-square"><Eye size={16} /></button>
                        </div>
                    </SettingItem>
                    <SettingItem
                        label="Websocket Compression"
                        description="Reduce latency for high-frequency data streams."
                    >
                        <input type="checkbox" className="toggle toggle-info" defaultChecked />
                    </SettingItem>
                    <SettingItem
                        label="Data Bridge Sync"
                        description="Frequency of remote database synchronization."
                    >
                        <input type="range" min="0" max="100" value="80" className="range range-xs range-primary w-48" />
                    </SettingItem>
                </SettingsCard>

                {/* System Preferences */}
                <SettingsCard
                    title="SYSTEM_INTERFACE"
                    description="Customize terminal visuals and notification protocols."
                    icon={Zap}
                >
                    <SettingItem
                        label="UI Glassmorphism"
                        description="Enable complex transparency and blur effects (GPU Intensive)."
                    >
                        <input type="checkbox" className="toggle toggle-secondary" defaultChecked />
                    </SettingItem>
                    <SettingItem
                        label="Ambient 3D Engine"
                        description="Toggle background particle field and volumetric shapes."
                    >
                        <input type="checkbox" className="toggle toggle-primary" defaultChecked />
                    </SettingItem>
                    <SettingItem
                        label="Notification Audio"
                        description="Audible alerts for strategic trade execution events."
                    >
                        <button className="btn btn-sm btn-outline border-white border-opacity-10 text-xs font-black tracking-widest px-4 h-10">TEST_AUDIO</button>
                    </SettingItem>
                </SettingsCard>

                {/* Advanced Operational Stats */}
                <div className="glass-card p-8 border-opacity-10 bg-primary bg-opacity-5 flex flex-col justify-center border-primary border-opacity-20">
                    <div className="grid grid-cols-2 gap-8">
                        <div>
                            <p className="text-[10px] font-black text-primary uppercase tracking-[0.2em] mb-2">ENGINE_UPTIME</p>
                            <p className="text-3xl font-black text-white">422:12:09</p>
                        </div>
                        <div>
                            <p className="text-[10px] font-black text-primary uppercase tracking-[0.2em] mb-2">THERMAL_LOAD</p>
                            <p className="text-3xl font-black text-success">STABLE</p>
                        </div>
                        <div>
                            <p className="text-[10px] font-black text-primary uppercase tracking-[0.2em] mb-2">CPU_USAGE</p>
                            <p className="text-3xl font-black text-white">12.4%</p>
                        </div>
                        <div>
                            <p className="text-[10px] font-black text-primary uppercase tracking-[0.2em] mb-2">MEM_POOL</p>
                            <p className="text-3xl font-black text-white">2.4 GB</p>
                        </div>
                    </div>
                    <div className="mt-10 pt-10 border-t border-primary border-opacity-10">
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center animate-pulse">
                                <Cpu className="text-white" size={20} />
                            </div>
                            <p className="text-xs font-black text-primary uppercase tracking-widest">Core Engine Heartbeat: ACTIVE</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SettingsPage;
