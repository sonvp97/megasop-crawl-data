import axios from "axios";
import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  TextField,
  useTheme,
  Modal,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  IconButton,
  Link,
  CircularProgress,
} from "@mui/material";
import Header from "components/Header";
import { DataGrid } from "@mui/x-data-grid";
import { API_BASE_URL } from "scenes/api/api";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import CloseIcon from "@mui/icons-material/Close";
import FilterAltIcon from "@mui/icons-material/FilterAlt";
function Search() {
  const authToken = JSON.parse(JSON.stringify(localStorage.getItem("token")));
  const [data, setData] = useState([]);
  const [paginationModel, setPaginationModel] = React.useState({
    pageSize: 10,
    page: 0,
  });
  const [dataReport, setDataReport] = useState([]);
  const [paginationModelReport, setPaginationModelReport] = React.useState({
    pageSize: 10,
    page: 0,
  });
  const [totalRows, setTotalRows] = useState(0);
  const [totalRowReport, setTotalRowReport] = useState(0);
  const [idDetail, setIdDetail] = useState("");
  const [idBrand, setIdBrand] = useState("");
  const [loading, setLoading] = useState(false);

  const theme = useTheme();
  const [report, setReport] = useState(false);
  const [openReport, setOpenReport] = useState(false);

  const [fromDate, setFromDate] = useState(new Date());
  const [toDate, setToDate] = useState(new Date());
  const [status, setStatus] = useState("");
  const [brand, setBrand] = useState(null);

  const handleStatusChange = (event) => {
    setStatus(event.target.value);
  };

  const handleBrandChange = (event) => {
    if (event.target.value == 0) {
      setBrand(null);
    } else {
      setBrand(event.target.value);
    }
  };
  const handleTime1Change = (newValue) => {
    setFromDate(newValue.$d);
  };

  const handleSearchReportDetail = () => {
    handleBrandClick(idDetail);
  };
  const handleTime2Change = (newValue) => {
    setToDate(newValue.$d);
  };
  useEffect(() => {
    getListReport();
  }, [paginationModel.page, paginationModel.pageSize, report]);
  useEffect(() => {
    if (openReport) {
      handleBrandClick(idDetail);
    }
  }, [paginationModelReport.page, paginationModelReport.pageSize]);
  const getListReport = async () => {
    setLoading(true);
    try {
      const skip = paginationModel.page * paginationModel.pageSize;
      const limit = paginationModel.pageSize;
      const from_date = fromDate;
      const to_date = toDate;
      const brand_id = brand;
      const response = await axios.get(API_BASE_URL + "/report", {
        params: {
          from_date,
          to_date,
          brand_id,
          skip,
          limit,
        },
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      console.log(response.data);
      setData(response.data.listReport);
      setTotalRows(response.data.count);
    } catch (error) {}
    setLoading(false);
  };
  const handleSearchReport = (e) => {
    setReport(!report);
  };
  const handleCloseReport = async () => {
    setOpenReport(false);
    setStatus("");
  };
  const handleBrandClick = async (id) => {
    setOpenReport(true);
    setIdDetail(id);
    const clickedObject = data.find((item) => item.id === id);
    setIdBrand(clickedObject.brand_id);
    try {
      const skip = paginationModelReport.page * paginationModelReport.pageSize;
      const limit = paginationModelReport.pageSize;
      const report_id = clickedObject.report_id;
      const brand_id = clickedObject.brand_id;
      const response = await axios.get(API_BASE_URL + "/report/detail", {
        params: {
          skip,
          limit,
          report_id,
          status,
          brand_id,
        },
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      console.log(response.data.listReportDetail);
      setDataReport(response.data.listReportDetail);
      setTotalRowReport(response.data.count);
    } catch (error) {}
  };

  const brandNames = {
    0: "None",
    1: "Hasaki",
    2: "Pharmacity",
    3: "Guardian",
    4: "Watson",
  };
  const statusNames = {
    0: "FAILURE",
    1: "SUCCESS",
  };
  const columnReportDetail = [
    {
      field: "id",
      headerName: "#",
      width: 40,
      align: "center",
      headerAlign: "center",
    },
    {
      field: "name",
      headerName: "Name",
      width: 450,
      renderCell: (params) => (
        <Link
          href={params.value}
          target="_blank"
          rel="noopener"
          sx={{ color: "white", textDecoration: "none" }}
          style={{ whiteSpace: "pre-wrap" }}
        >
          {params.value}
        </Link>
      ),
    },
    {
      field: "status",
      headerName: "Status",
      width: 200,
      valueGetter: (params) => statusNames[params.value] || "",
    },
    {
      field: "time",
      headerName: "Crawl Time",
      width: 200,
    },
  ];
  const columns = [
    {
      field: "id",
      headerName: "#",
      width: 40,
      align: "center",
      headerAlign: "center",
    },
    {
      field: "brand_id",
      headerName: "Name Brand",
      width: 200,
      renderCell: (params) => {
        const brandName = brandNames[params.value] || "";
        return (
          <div
            style={{ cursor: "pointer" }}
            onClick={() => handleBrandClick(params.id)}
          >
            {brandName}
          </div>
        );
      },
    },
    {
      field: "total",
      headerName: "Total Link",
      width: 200,
    },
    {
      field: "success",
      headerName: "Success",
      width: 150,
    },
    {
      field: "failure",
      headerName: "Failure",
      width: 150,
    },
    {
      field: "start_crawl",
      headerName: "Start Crawl",
      width: 200,
    },
    {
      field: "end_crawl",
      headerName: "End Crawl",
      width: 200,
    },
  ];

  return (
    <>
      <Box m="1.5rem 1.8rem">
        <Header title="Report" />
        <Box
          mt="40px"
          height="75vh"
          sx={{
            "& .MuiDataGrid-root": {
              border: "none",
            },
            "& .MuiDataGrid-cell": {
              borderBottom: "none",
            },
            "& .MuiDataGrid-columnHeaders": {
              backgroundColor: theme.palette.background.alt,
              color: theme.palette.secondary[100],
              borderBottom: "none",
            },
            "& .MuiDataGrid-virtualScroller": {
              backgroundColor: theme.palette.primary.light,
            },
            "& .MuiDataGrid-footerContainer": {
              backgroundColor: theme.palette.background.alt,
              color: theme.palette.secondary[100],
              borderTop: "none",
            },
            "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
              color: `${theme.palette.secondary[200]} !important`,
            },
            "& .image": {
              borderRadius: "50%",
            },
            "& .MuiDataGrid-checkboxInput.Mui-checked": {
              color: "white",
            },
            "& .MuiDataGrid-root--densityStandard": {
              maxHeight: "559.2px",
            },
            "& .css-z35w7p": {
              height: "40px",
              marginRight: "5px"
            },
          }}
        >
          <Box sx={{ display: "flex", mr: 3, mb: 2, alignItems: "center" }}>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker
                label="From Date"
                value={fromDate}
                onChange={handleTime1Change}
                renderInput={(params) => <TextField {...params} />}
                format="yyyy-MM-dd"
              />
              <DatePicker
                label="To Date"
                value={toDate}
                onChange={handleTime2Change}
                renderInput={(params) => <TextField {...params} />}
                format="yyyy-MM-dd"
              />
            </LocalizationProvider>
            <FormControl sx={{ minWidth: "150px" }}>
              <InputLabel id="brand-select-label" sx={{ top: "-5px" }}>
                Brand
              </InputLabel>
              <Select
                labelId="brand-select-label"
                id="brand-select"
                label="brand"
                value={brand}
                sx={{ height: "40px" }}
                onChange={handleBrandChange}
              >
                {Object.entries(brandNames).map(([key, value]) => (
                  <MenuItem key={key} value={key}>
                    {value}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <IconButton
              onClick={handleSearchReport}
              sx={{
                width: 50,
                height: 50,
              }}
            >
              {loading ? <CircularProgress size={24} /> : <FilterAltIcon />}
            </IconButton>
          </Box>
          <DataGrid
            rows={data ? data : []}
            columns={columns}
            paginationModel={paginationModel}
            onPaginationModelChange={setPaginationModel}
            pageSizeOptions={[10, 20, 30]}
            rowCount={totalRows}
            paginationMode="server"
          />
          <Modal open={openReport} onClose={handleCloseReport}>
            <Box
              sx={{
                position: "absolute",
                top: 0,
                right: 0,
                width: "calc(100% - 500px)",
                height: "calc(100% - 80px)",
                bgcolor: theme.palette.primary[700],
                borderRadius: "8px 0 0 0",
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
                p: 4,
              }}
            >
              <Header title={brandNames[idBrand]} />
              <IconButton
                sx={{ position: "absolute", top: 0, right: 0 }}
                onClick={handleCloseReport}
              >
                <CloseIcon />
              </IconButton>
              <Box sx={{ display: "flex", mr: 3, mb: 2 }}>
                <FormControl sx={{ mb: 2, minWidth: "150px", mt: 3 }}>
                  <InputLabel id="status-select-label" sx={{ top: "-5px" }}>
                    Status
                  </InputLabel>
                  <Select
                    labelId="status-select-label"
                    id="status-select"
                    label="Status"
                    value={status}
                    sx={{ height: "40px" }}
                    onChange={handleStatusChange}
                  >
                    <MenuItem value="">None</MenuItem>
                    <MenuItem value="0">FAILURE</MenuItem>
                    <MenuItem value="1">SUCCESS</MenuItem>
                  </Select>
                </FormControl>
                <IconButton
                  sx={{ width: 50, height: 50, top: 20 }}
                  onClick={handleSearchReportDetail}
                >
                  {loading ? <CircularProgress size={24} /> : <FilterAltIcon />}
                </IconButton>
              </Box>
              <DataGrid
                rows={dataReport ? dataReport : []}
                columns={columnReportDetail}
                paginationModel={paginationModelReport}
                onPaginationModelChange={setPaginationModelReport}
                pageSizeOptions={[10, 20, 30]}
                rowCount={totalRowReport}
                paginationMode="server"
                sx={{ height: "calc(100% - 150px)" }}
              />
            </Box>
          </Modal>
        </Box>
      </Box>
    </>
  );
}

export default Search;
