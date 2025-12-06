import { Outlet, NavLink } from "react-router-dom";
import { Home, Users, UserCheck, FileText } from "lucide-react";

export default function Layout() {

    const navItems = [
        { name: "Dashboard", path: "/dashboard", icon: <Home size={20} /> },
        { name: "Residentes", path: "/residentes", icon: <Users size={20} /> },
        { name: "Reportes", path: "/reportes", icon: <FileText size={20} /> },
        { name: "Entrenamiento", path: "/entrenamiento", icon: <FileText size={20} /> },
        { name: "Cámara", path: "/camera", icon: <FileText size={20} /> },
    ];

    return (
        <div className="flex h-screen w-full bg-gray-100">
            
            {/* SIDEBAR ALWAYS OPEN */}
            <aside className="bg-white shadow-xl border-r w-64 flex flex-col">
                
                {/* TOP AREA */}
                <div className="flex items-center justify-center p-4 h-16 border-b">
                    <h1 className="text-xl font-bold">ResidencialID</h1>
                </div>

                {/* NAVIGATION */}
                <nav className="mt-4 flex flex-col gap-1 px-2">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                `
                                flex items-center gap-3 p-3 rounded-xl
                                transition font-medium
                                ${
                                    isActive
                                        ? "bg-blue-100 text-blue-700 font-semibold"
                                        : "hover:bg-gray-200"
                                }
                                `
                            }
                        >
                            {item.icon}
                            <span>{item.name}</span>
                        </NavLink>
                    ))}
                </nav>
            </aside>

            {/* MAIN CONTENT */}
            <main className="flex-1 overflow-y-auto">
                <header className="w-full bg-white shadow p-4 flex items-center justify-between">
                    <h2 className="text-lg font-semibold"></h2>
                </header>

                <div className="p-6">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
