import Link from "next/link";
import { User, Wrench } from "lucide-react";

export default function RegisterPage() {
    return (
        <div className="space-y-8">
            <div className="text-center space-y-2">
                <h1 className="text-2xl font-bold text-secondary">Crea un account</h1>
                <p className="text-neutral-500 text-sm">Come vuoi usare Pronto Casa?</p>
            </div>

            <div className="grid gap-4">
                <Link href="/auth/register/client" className="block group">
                    <div className="flex items-center gap-4 p-4 rounded-xl border-2 border-neutral-100 hover:border-primary/50 hover:bg-orange-50 transition-all cursor-pointer">
                        <div className="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center text-primary group-hover:scale-110 transition-transform">
                            <User className="w-6 h-6" />
                        </div>
                        <div className="text-left">
                            <h3 className="font-bold text-secondary">Sono un Cliente</h3>
                            <p className="text-xs text-neutral-500">Ho bisogno di una riparazione</p>
                        </div>
                    </div>
                </Link>

                <Link href="/auth/register/technician" className="block group">
                    <div className="flex items-center gap-4 p-4 rounded-xl border-2 border-neutral-100 hover:border-secondary/50 hover:bg-sky-50 transition-all cursor-pointer">
                        <div className="w-12 h-12 rounded-full bg-sky-100 flex items-center justify-center text-secondary group-hover:scale-110 transition-transform">
                            <Wrench className="w-6 h-6" />
                        </div>
                        <div className="text-left">
                            <h3 className="font-bold text-secondary">Sono un Tecnico</h3>
                            <p className="text-xs text-neutral-500">Voglio offrire i miei servizi</p>
                        </div>
                    </div>
                </Link>
            </div>

            <div className="text-center text-sm text-neutral-600">
                Hai già un account?{" "}
                <Link href="/auth/login" className="font-bold text-primary hover:underline">
                    Accedi
                </Link>
            </div>
        </div>
    );
}
