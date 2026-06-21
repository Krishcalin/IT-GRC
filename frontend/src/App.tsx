import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthContext, useAuthProvider, useAuth } from './hooks/useAuth'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ControlsPage from './pages/ControlsPage'
import ControlDetailPage from './pages/ControlDetailPage'
import ClausesPage from './pages/ClausesPage'
import ClauseDetailPage from './pages/ClauseDetailPage'
import DocumentsPage from './pages/DocumentsPage'
import DocumentDetailPage from './pages/DocumentDetailPage'
import InterestedPartiesPage from './pages/InterestedPartiesPage'
import ObjectivesPage from './pages/ObjectivesPage'
import ObjectiveDetailPage from './pages/ObjectiveDetailPage'
import MetricsPage from './pages/MetricsPage'
import MetricDetailPage from './pages/MetricDetailPage'
import SuppliersPage from './pages/SuppliersPage'
import SupplierDetailPage from './pages/SupplierDetailPage'
import IncidentsPage from './pages/IncidentsPage'
import IncidentDetailPage from './pages/IncidentDetailPage'
import TrainingPage from './pages/TrainingPage'
import CampaignDetailPage from './pages/CampaignDetailPage'
import RisksPage from './pages/RisksPage'
import SoAPage from './pages/SoAPage'
import EvidencePage from './pages/EvidencePage'
import AuditsPage from './pages/AuditsPage'
import AuditDetailPage from './pages/AuditDetailPage'
import PoliciesPage from './pages/PoliciesPage'
import AssetsPage from './pages/AssetsPage'

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth()
  if (loading) return <div className="flex items-center justify-center h-screen"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" /></div>
  if (!user) return <Navigate to="/login" replace />
  return <>{children}</>
}

const App: React.FC = () => {
  const auth = useAuthProvider()

  return (
    <AuthContext.Provider value={auth}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route index element={<DashboardPage />} />
          <Route path="controls" element={<ControlsPage />} />
          <Route path="controls/:id" element={<ControlDetailPage />} />
          <Route path="clauses" element={<ClausesPage />} />
          <Route path="clauses/:id" element={<ClauseDetailPage />} />
          <Route path="documents" element={<DocumentsPage />} />
          <Route path="documents/:id" element={<DocumentDetailPage />} />
          <Route path="interested-parties" element={<InterestedPartiesPage />} />
          <Route path="objectives" element={<ObjectivesPage />} />
          <Route path="objectives/:id" element={<ObjectiveDetailPage />} />
          <Route path="metrics" element={<MetricsPage />} />
          <Route path="metrics/:id" element={<MetricDetailPage />} />
          <Route path="suppliers" element={<SuppliersPage />} />
          <Route path="suppliers/:id" element={<SupplierDetailPage />} />
          <Route path="incidents" element={<IncidentsPage />} />
          <Route path="incidents/:id" element={<IncidentDetailPage />} />
          <Route path="training" element={<TrainingPage />} />
          <Route path="training/:id" element={<CampaignDetailPage />} />
          <Route path="risks" element={<RisksPage />} />
          <Route path="soa" element={<SoAPage />} />
          <Route path="evidence" element={<EvidencePage />} />
          <Route path="audits" element={<AuditsPage />} />
          <Route path="audits/:id" element={<AuditDetailPage />} />
          <Route path="policies" element={<PoliciesPage />} />
          <Route path="assets" element={<AssetsPage />} />
        </Route>
      </Routes>
    </AuthContext.Provider>
  )
}

export default App
