import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell } from "@/components/ui/table";

export default function AppStoreDataTool() {
  const [csvData, setCsvData] = useState([]);
  const [totals, setTotals] = useState({});

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const rows = text.trim().split("\n").map((row) => row.split(","));
      const headers = rows[0];
      const data = rows.slice(1);

      const numericTotals = {};
      headers.forEach((header, i) => {
        let total = 0;
        let isNumeric = true;
        for (let row of data) {
          const val = parseFloat(row[i]);
          if (!isNaN(val)) total += val;
          else isNumeric = false;
        }
        if (isNumeric) numericTotals[header] = total;
      });

      setCsvData([headers, ...data]);
      setTotals(numericTotals);
    };
    reader.readAsText(file);
  };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">📊 App Store Data Analyzer</h1>
      <Input type="file" accept=".csv" onChange={handleFileUpload} />

      {csvData.length > 0 && (
        <Card>
          <CardContent>
            <h2 className="text-xl font-semibold mb-4">Preview</h2>
            <div className="overflow-auto max-h-[400px]">
              <Table>
                <TableHead>
                  <TableRow>
                    {csvData[0].map((header, i) => (
                      <TableHeaderCell key={i}>{header}</TableHeaderCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {csvData.slice(1, 11).map((row, i) => (
                    <TableRow key={i}>
                      {row.map((cell, j) => (
                        <TableCell key={j}>{cell}</TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      )}

      {Object.keys(totals).length > 0 && (
        <Card>
          <CardContent>
            <h2 className="text-xl font-semibold mb-4">Column Totals</h2>
            <ul className="list-disc pl-6">
              {Object.entries(totals).map(([header, total], i) => (
                <li key={i}>
                  <strong>{header}:</strong> {total.toLocaleString()}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
