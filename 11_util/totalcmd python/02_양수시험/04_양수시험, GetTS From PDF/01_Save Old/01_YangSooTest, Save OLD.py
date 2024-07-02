# def make_cell_values(self, row_index):
#     row_data = self.get_excel_row(row_index)
#
#     len_row_data = len(row_data)
#     print('len(row_data):', len_row_data)
#
#     address = row_data[1]
#     hp = row_data[2]
#     casing = row_data[3]
#     well_rad = row_data[4]
#     simdo = row_data[5]
#     q = row_data[6]
#     natural = row_data[7]
#     stable = row_data[8]
#
#     project_name = ''
#     jigu_name = ''
#     company_name = ''
#     self.STABLE_TIME = row_data[12]
#
#     if len_row_data > 9:
#         project_name = row_data[9]
#         jigu_name = row_data[10]
#         company_name = row_data[11]
#
#     # 2024년 6월 15일 추가
#     # 조사명, 지구명을 추가해줌,  YanSoo.xlsx 파일에 ...
#
#     # 안정수위가 자연수위보다 낮을경우 .... 자연수위와 안정수위를 바꿔 준다. 에러방지를 위해서
#     if stable < natural:
#         natural = row_data[7]
#         stable = row_data[6]
#
#     gong = self.extract_number(row_data[0])
#     str_gong = f"공  번 : W - {gong}"
#
#     time.sleep(1)
#
#     if len_row_data <= 9:
#         return {"J48": str_gong, "I46": address, "I52": casing, "I48": hp, "M44": well_rad, "M45": simdo,
#                 "M48": natural, "M49": stable, "M51": q}
#     else:
#         return {"J48": str_gong, "I46": address, "I52": casing, "I48": hp, "M44": well_rad, "M45": simdo,
#                 "M48": natural, "M49": stable, "M51": q, "I44": project_name, "I45": jigu_name, "I47": company_name}

# def _inject_input(self, wb):
#     ws = wb.Worksheets("Input")
#     ws.Activate()
#     time.sleep(1)
#     self.inject_value_to_cells(wb)
#
#     time.sleep(1)
#
#     if self.isit_oldversion(ws, "CommandButton2"):
#         self.click_excel_button(ws, "CommandButton2")
#         print('_inject_input -- SetCB1 ')
#         time.sleep(1)
#
#         self.click_excel_button(ws, "CommandButton3")
#         print('_inject_input -- SetCB2 ')
#         time.sleep(1)
#
#         self.click_excel_button(ws, "CommandButton6")
#         print('_inject_input -- Chart ')
#         time.sleep(1)
#
#         self.click_excel_button(ws, "CommandButton1")
#         print('_inject_input -- PumpingTest ')
#         time.sleep(1)
#     else:
#         self.click_excel_button(ws, "CommandButton_CB1")
#         print('_inject_input -- SetCB1 ')
#         time.sleep(1)
#
#         self.click_excel_button(ws, "CommandButton_CB2")
#         print('_inject_input -- SetCB2 ')
#         time.sleep(1)
#
#         self.click_excel_button(ws, "CommandButton_Chart")
#         print('_inject_input -- SetChart ')
#         time.sleep(1)


# def _inject_long_term_test(self, wb, excel):
#     ws = wb.Worksheets("LongTest")
#     ws.Activate()
#     values = [540, 600, 660, 720, 780, 840]
#
#     # Clear GoalSeekTarget
#     ws.Range("GoalSeekTarget").Value = 0
#
#     if self.STABLE_TIME == 0:
#         selected_value = random.choice(values)
#     else:
#         selected_value = self.STABLE_TIME
#
#     if self.debug_yes: print(f'stable time selection ... : {selected_value}')
#
#     print('_inject_long_term_test -- Reset 0.1')
#     self.click_excel_button(ws, "CommandButton5")  # Reset 0.1
#     time.sleep(1)
#
#     ws.OLEObjects("ComboBox1").Object.Value = selected_value
#     time.sleep(1)
#
#     print('_inject_long_term_test -- excel.Application.Run("mod_W1LongtermTEST.TimeSetting")')
#
#     # in Excel File , ModuleName CHanged, so it treat multi module name
#     self.ExcelApplicationMoudule(excel, ["mod_W1LongtermTEST", "mod_W1_LongtermTEST"])
#
#     print('_inject_long_term_test -- Reset 0.1')
#     self.click_excel_button(ws, "CommandButton5")  # Reset 0.1
#     time.sleep(1)
#
#     print('_inject_long_term_test -- FindAnswer')
#     self.click_excel_button(ws, "CommandButton4")  # Find Answer
#     time.sleep(2)
#
#     print('_inject_long_term_test -- Check')
#     self.click_excel_button(ws, "CommandButton7")  # Check
#
# @staticmethod
# def ExcelApplicationMoudule(excel, module_names):
#     for module_name in module_names:
#         try:
#             excel.Application.Run(module_name + ".TimeSetting")
#             time.sleep(1)
#             print(f"Application.Run, {module_name} is running successfully")
#
#         except Exception as e:
#             print(f"Application.Run, {module_name} is not found .... ", e)
#             time.sleep(1)  # Optional: Wait a bit before retrying