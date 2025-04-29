import jsPDF from 'jspdf';
import 'jspdf-autotable';
import * as XLSX from 'xlsx';

export const exportToPDF = (data: any[]) => {
  const doc = new jsPDF();
  
  // Título
  doc.setFontSize(18);
  doc.text('Reporte de Evaluación de KPIs', 14, 20);
  
  // Fecha
  doc.setFontSize(11);
  doc.text(`Fecha: ${new Date().toLocaleDateString()}`, 14, 30);

  // Tabla
  const tableColumn = ["Empleado", "Departamento", "KPI 1", "KPI 2", "KPI 3", "Promedio"];
  const tableRows = data.map(item => [
    item.empleado,
    item.departamento,
    item.kpi1,
    item.kpi2,
    item.kpi3,
    item.promedio
  ]);

  (doc as any).autoTable({
    head: [tableColumn],
    body: tableRows,
    startY: 40,
    theme: 'grid',
    styles: {
      fontSize: 8,
      cellPadding: 3,
      lineColor: [0, 0, 0],
      lineWidth: 0.1,
    },
    headStyles: {
      fillColor: [44, 83, 100],
      textColor: [255, 255, 255],
      fontStyle: 'bold'
    }
  });

  doc.save('evaluacion-kpis.pdf');
};

export const exportToExcel = (data: any[]) => {
  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Evaluaciones");
  XLSX.writeFile(workbook, 'evaluacion-kpis.xlsx');
};
