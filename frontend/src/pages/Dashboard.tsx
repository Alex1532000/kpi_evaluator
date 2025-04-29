import React from 'react';
import {
  Box,
  Button,
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Stack
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { exportToPDF, exportToExcel } from '../utils/exportUtils';

// Datos de ejemplo
const evaluationData = [
  {
    id: 1,
    empleado: "Juan Pérez",
    departamento: "Ventas",
    kpi1: 95,
    kpi2: 88,
    kpi3: 92,
    promedio: 91.67
  },
  {
    id: 2,
    empleado: "María García",
    departamento: "Marketing",
    kpi1: 87,
    kpi2: 90,
    kpi3: 85,
    promedio: 87.33
  }
];

const Dashboard: React.FC = () => {
  const handleEvaluate = () => {
    console.log('Evaluando...');
  };

  const handleExportPDF = () => {
    exportToPDF(evaluationData);
  };

  const handleExportExcel = () => {
    exportToExcel(evaluationData);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        {/* Encabezado con título y botones */}
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          mb: 3,
          flexWrap: 'wrap',
          gap: 2
        }}>
          <Typography variant="h4" component="h1">
            Evaluaciones de KPIs
          </Typography>
          
          <Stack direction="row" spacing={2}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<AssessmentIcon />}
              onClick={handleEvaluate}
            >
              Evaluar
            </Button>
            
            <Button
              variant="contained"
              color="secondary"
              startIcon={<PictureAsPdfIcon />}
              onClick={handleExportPDF}
            >
              PDF
            </Button>
            
            <Button
              variant="contained"
              color="success"
              startIcon={<DownloadIcon />}
              onClick={handleExportExcel}
            >
              Excel
            </Button>
          </Stack>
        </Box>

        {/* Tabla de evaluaciones */}
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Empleado</TableCell>
                <TableCell>Departamento</TableCell>
                <TableCell align="right">KPI 1</TableCell>
                <TableCell align="right">KPI 2</TableCell>
                <TableCell align="right">KPI 3</TableCell>
                <TableCell align="right">Promedio</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {evaluationData.map((row) => (
                <TableRow key={row.id}>
                  <TableCell>{row.empleado}</TableCell>
                  <TableCell>{row.departamento}</TableCell>
                  <TableCell align="right">{row.kpi1}%</TableCell>
                  <TableCell align="right">{row.kpi2}%</TableCell>
                  <TableCell align="right">{row.kpi3}%</TableCell>
                  <TableCell align="right">{row.promedio.toFixed(2)}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Container>
  );
};

export default Dashboard;
