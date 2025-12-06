import Layout from "../features/layout/Layout.jsx";

import Dashboard from "../features/dashboard/Dashboard.jsx";
import Residentes from "../features/residentes/pages/ResidentsManagement.jsx";
import Entrenamiento from "../features/training/pages/TrainingPage.jsx";
import CameraView from "../features/cameraView/CameraView.jsx";
import AccessTable from "../features/reportes/AccessTable.tsx";

const routes = [
    {
        path: "/",
        element: <Layout />,
        children: [
            {
                path: "dashboard",
                element: <Dashboard />,
            },
            {
                path: "residentes",
                element: <Residentes />,
            },
            {
                path: "entrenamiento",
                element: <Entrenamiento />,
            },
            {
                path: "camera",
                element: <CameraView />,
            },
            {
                path: "reportes",
                element: <AccessTable />,
            }
        ],
    },
];

export default routes;
