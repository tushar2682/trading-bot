import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../../services/api';
import {
    Globe,
    UserPlus,
    Mail,
    Lock,
    ShieldCheck,
    CheckSquare,
    ArrowRight,
    User,
    Fingerprint,
    Cpu
} from 'lucide-react';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await authService.register(formData);
            navigate('/login');
        } catch (err) {
            console.error("Provisioning failed", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden">
            <div className="max-w-[500px] w-full relative z-10">
                {/* Brand Header */}
                <div className="flex flex-col items-center mb-12 text-center">
                    <div className="w-24 h-24 bg-primary bg-opacity-10 rounded-[2rem] flex items-center justify-center mb-8 border border-primary border-opacity-20 shadow-2xl shadow-primary/20 backdrop-blur-xl">
                        <Fingerprint className="text-primary" size={48} />
                    </div>
                    <h1 className="text-5xl font-black tracking-tighter text-white elite-gradient-text leading-tight mb-4">IDENTITY_PROVISION</h1>
                    <p className="text-slate-500 font-bold text-sm uppercase tracking-[0.3em]">Operator Onboarding Protocol</p>
                </div>

                {/* Register Card */}
                <div className="glass-card p-12 overflow-hidden relative">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="form-control space-y-3">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Alias_Designation</label>
                            <div className="relative group">
                                <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors" size={20} />
                                <input
                                    type="text"
                                    required
                                    value={formData.username}
                                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                    className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary pl-12 h-16 rounded-2xl font-bold text-white placeholder:text-slate-700"
                                    placeholder="e.g. ALPHA_OPERATOR_01"
                                />
                            </div>
                        </div>

                        <div className="form-control space-y-3">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Communication_Sync</label>
                            <div className="relative group">
                                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors" size={20} />
                                <input
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary pl-12 h-16 rounded-2xl font-bold text-white placeholder:text-slate-700"
                                    placeholder="operator@nebu-corp.global"
                                />
                            </div>
                        </div>

                        <div className="form-control space-y-3">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Security_Cipher</label>
                            <div className="relative group">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors" size={20} />
                                <input
                                    type="password"
                                    required
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary pl-12 h-16 rounded-2xl font-bold text-white placeholder:text-slate-700"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <div className="p-5 bg-primary bg-opacity-5 rounded-2xl border border-primary border-opacity-10 flex items-start gap-4">
                            <CheckSquare className="text-primary mt-1 shrink-0" size={18} />
                            <p className="text-[10px] font-bold text-slate-400 leading-relaxed uppercase tracking-tight">
                                I verify operational compliance and accept real-time monitoring of all terminal interactions.
                            </p>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className={`btn btn-primary w-full h-18 rounded-2xl text-xs font-black uppercase tracking-[0.3em] shadow-lg shadow-primary/20 transition-all duration-300 mt-4 ${loading ? 'loading' : ''}`}
                        >
                            {loading ? 'PROVISIONING...' : 'INITIALIZE_IDENTITY'}
                            {!loading && <ArrowRight size={20} className="ml-2" />}
                        </button>
                    </form>

                    <div className="mt-12 pt-8 border-t border-white border-opacity-5 text-center">
                        <p className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">
                            Already Authorized? <Link to="/login" className="text-primary hover:text-white transition-colors font-black underline underline-offset-8 tracking-widest">SECURE_LOGIN</Link>
                        </p>
                    </div>
                </div>
            </div>

            {/* Background Decoration */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary opacity-[0.03] rounded-full blur-[120px] pointer-events-none" />
        </div>
    );
};

export default Register;
