FUNCTION FUN_0003427c @ 0003427c


int * FUN_0003427c(undefined4 param_1,int param_2,int param_3)

{
  bool bVar1;
  undefined *puVar2;
  int *piVar3;
  code *pcVar4;
  int iVar5;
  int *piVar6;
  code *pcVar7;
  undefined4 uVar8;
  uint uVar9;
  int iVar10;
  undefined *puVar11;
  undefined4 uVar12;
  int *piVar13;
  int *piVar14;
  int *piVar15;
  code *local_7c [2];
  int local_74;
  int *local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  code *local_60;
  int *local_5c;
  int *local_58 [2];
  code *local_50;
  code *local_4c;
  code *local_48;
  code *local_44;
  undefined4 *local_40;
  undefined4 *local_3c;
  code *local_38;
  undefined *local_34;
  int local_30;
  undefined *local_2c;
  
  puVar2 = PTR_DAT_0005229c;
  local_7c[0] = (code *)0x0;
  local_7c[1] = (code *)0x0;
  local_74 = 0;
  uVar9 = *(uint *)(param_2 + 8);
  if (param_3 != 0) {
    if (uVar9 < 5) {
                    /* WARNING: Could not emulate address calculation at 0x000342dc */
                    /* WARNING: Treating indirect jump as call */
      piVar3 = (int *)(*(code *)(&_gp_1 + *(int *)(PTR_DAT_000522ac + uVar9 * 4 + -0x1498)))();
      return piVar3;
    }
switchD_000342e8_default:
    FUN_0001859c(PTR_DAT_000522ac + -0x1d08,1,4,4,*(undefined4 *)(param_2 + 8));
    FUN_0001ac3c(PTR_DAT_000522ac + -0x1d30,0x1b31,0xa3,PTR_DAT_000522ac + -0x2380);
    return (int *)0x0;
  }
  if (uVar9 != 4) goto switchD_000342e8_default;
  local_4c = *(code **)(param_2 + 0xc);
  pcVar4 = *(code **)(param_2 + 0x10);
  local_7c[1] = *(code **)(param_2 + 0x14);
  local_74 = *(int *)(param_2 + 0x18);
  local_58[0] = (int *)0x0;
  local_5c = (int *)0x0;
  local_50 = (code *)(PTR_LAB_000522a8 + -0x74a0);
  local_60 = (code *)0x0;
  local_64 = 0;
  local_68 = 0;
  local_6c = 0;
  local_70 = (int *)0x0;
  local_7c[0] = pcVar4;
  local_48 = local_7c[1];
  local_30 = local_74;
  local_5c = (int *)FUN_00018b60(local_4c,*(undefined4 *)(PTR_DAT_0005229c + 0x2c0c));
  local_2c = puVar2;
  if (local_5c == (int *)0x0) {
    uVar12 = 0x1b5e;
    piVar3 = (int *)0x0;
LAB_000355f4:
    pcVar4 = (code *)0x0;
    piVar13 = (int *)0x0;
    piVar6 = (int *)0x0;
    piVar15 = (int *)0x0;
    local_50 = (code *)0x0;
    uVar8 = 0xa4;
  }
  else {
    local_60 = (code *)(*local_50)(local_5c,*(undefined4 *)(PTR_DAT_0005229c + 0x2dd8));
    if (local_60 == (code *)0x0) {
      uVar12 = 0x1b60;
      piVar3 = (int *)0x0;
      goto LAB_000355f4;
    }
    FUN_00019ba8(local_5c);
    puVar2 = PTR_PyMethod_Type_00052528;
    local_5c = (int *)0x0;
    if ((*(undefined **)(local_60 + 4) == PTR_PyMethod_Type_00052528) &&
       (local_5c = *(int **)(local_60 + 0xc), local_5c != (int *)0x0)) {
      local_60 = *(code **)(local_60 + 8);
      *local_5c = *local_5c + 1;
      *(int *)local_60 = *(int *)local_60 + 1;
      FUN_00019ba8();
      if (local_5c == (int *)0x0) goto LAB_00034bfc;
      local_58[0] = (int *)FUN_0001e790();
    }
    else {
LAB_00034bfc:
      local_58[0] = (int *)FUN_0001e6dc(local_60);
    }
    FUN_0001a404(local_5c);
    local_5c = (int *)0x0;
    if (local_58[0] == (int *)0x0) {
      uVar12 = 0x1b6f;
      piVar3 = local_58[0];
      goto LAB_000355f4;
    }
    FUN_00019ba8(local_60);
    piVar3 = local_58[0];
    puVar11 = PTR_DAT_0005229c;
    local_60 = (code *)0x0;
    local_58[0] = (int *)0x0;
    local_58[0] = (int *)(*local_50)(local_4c,*(undefined4 *)(PTR_DAT_0005229c + 0x2b90));
    local_34 = puVar11;
    if (local_58[0] == (int *)0x0) {
      piVar6 = (int *)0x0;
      local_50 = (code *)0x0;
      pcVar4 = (code *)0x0;
      piVar13 = (int *)0x0;
      uVar12 = 0x1b7c;
      uVar8 = 0xa5;
      piVar15 = (int *)0x0;
    }
    else {
      iVar5 = (*(code *)PTR_PyObject_SetItem_0005254c)(local_58[0],local_48,piVar3);
      uVar12 = 0x1b7e;
      if (iVar5 < 0) {
        uVar8 = 0xa5;
        piVar6 = (int *)0x0;
        local_50 = (code *)0x0;
        pcVar4 = (code *)0x0;
        piVar13 = (int *)0x0;
        piVar15 = (int *)0x0;
      }
      else {
        FUN_00019ba8(local_58[0]);
        local_58[0] = (int *)0x0;
        local_44 = (code *)(*(code *)PTR__PyThreadState_UncheckedGet_00052510)();
        local_40 = &local_68;
        local_3c = &local_64;
        local_38 = (code *)(PTR_LAB_000522a8 + -0x7088);
        FUN_00018f78(local_44,local_3c,local_40,&local_6c);
        local_60 = (code *)(*local_50)(local_4c,*(undefined4 *)(PTR_DAT_0005229c + 0x2d70));
        if (local_60 == (code *)0x0) {
          piVar15 = (int *)0x0;
          uVar12 = 0x1b98;
          iVar5 = 0;
        }
        else {
          local_5c = (int *)(*local_50)(local_60,*(undefined4 *)(PTR_DAT_0005229c + 0x2b68));
          if (local_5c == (int *)0x0) {
            piVar15 = (int *)0x0;
            uVar12 = 0x1b9a;
            iVar5 = 0;
          }
          else {
            FUN_00019ba8(local_60);
            local_60 = (code *)0x0;
            local_60 = (code *)(*local_50)(local_4c,*(undefined4 *)(PTR_DAT_0005229c + 0x2b48));
            if (local_60 == (code *)0x0) {
              piVar15 = (int *)0x0;
              uVar12 = 0x1b9d;
              iVar5 = 0;
            }
            else {
              iVar5 = (*(code *)PTR_PyObject_Size_000523cc)(pcVar4);
              if (iVar5 == -1) {
                uVar12 = 0x1b9f;
                piVar15 = (int *)0x0;
                iVar5 = 0;
              }
              else {
                iVar5 = (*(code *)PTR_PyLong_FromSsize_t_0005244c)(iVar5);
                if (iVar5 == 0) {
                  piVar15 = (int *)0x0;
                  uVar12 = 0x1ba0;
                }
                else {
                  if ((undefined *)local_5c[1] == puVar2) {
                    piVar15 = (int *)local_5c[3];
                    iVar10 = 0;
                    if (piVar15 != (int *)0x0) {
                      local_5c = (int *)local_5c[2];
                      *piVar15 = *piVar15 + 1;
                      iVar10 = 1;
                      *local_5c = *local_5c + 1;
                      FUN_00019ba8();
                    }
                  }
                  else {
                    iVar10 = 0;
                    piVar15 = (int *)0x0;
                  }
                  if ((undefined *)local_5c[1] == PTR_PyFunction_Type_000523a4) {
                    local_7c[0] = local_60;
                    local_7c[1] = pcVar4;
                    local_74 = iVar5;
                    local_58[0] = (int *)FUN_0001d2c0(local_5c,local_7c + -iVar10);
                    if (local_58[0] != (int *)0x0) {
LAB_00034c80:
                      FUN_0001a404(piVar15);
                      FUN_00019ba8(local_60);
                      local_60 = (code *)0x0;
                      FUN_00019ba8(iVar5);
LAB_00034ca8:
                      FUN_00019ba8(local_5c);
                      local_5c = (int *)0x0;
                      FUN_00019ba8(local_58[0]);
                      local_58[0] = (int *)0x0;
                      FUN_0001a404(local_64);
                      local_64 = 0;
                      FUN_0001a404(local_68);
                      local_68 = 0;
                      FUN_0001a404(local_6c);
                      local_6c = 0;
                      local_5c = (int *)(*local_50)(piVar3,*(undefined4 *)
                                                            (PTR_DAT_0005229c + 0x2adc));
                      if (local_5c == (int *)0x0) {
                        uVar12 = 0x1c64;
                        local_50 = (code *)0x0;
                      }
                      else {
                        pcVar4 = (code *)(*local_50)(local_4c,*(undefined4 *)(local_2c + 0x2c0c));
                        if (pcVar4 == (code *)0x0) {
                          uVar12 = 0x1c66;
                          local_50 = pcVar4;
                        }
                        else {
                          local_44 = pcVar4;
                          local_60 = (code *)(*local_50)(pcVar4,*(undefined4 *)
                                                                 (PTR_DAT_0005229c + 0x2c94));
                          if (local_60 == (code *)0x0) {
                            uVar12 = 0x1c68;
                            local_50 = local_44;
                          }
                          else {
                            FUN_00019ba8(local_44);
                            if ((*(undefined **)(local_60 + 4) == puVar2) &&
                               (piVar15 = *(int **)(local_60 + 0xc), piVar15 != (int *)0x0)) {
                              local_60 = *(code **)(local_60 + 8);
                              *piVar15 = *piVar15 + 1;
                              *(int *)local_60 = *(int *)local_60 + 1;
                              FUN_00019ba8();
                              local_58[0] = (int *)FUN_0001e790(local_60,piVar15);
                            }
                            else {
                              local_58[0] = (int *)FUN_0001e6dc();
                              piVar15 = (int *)0x0;
                            }
                            FUN_0001a404(piVar15);
                            if (local_58[0] == (int *)0x0) {
                              uVar12 = 0x1c77;
                              local_50 = (code *)0x0;
                            }
                            else {
                              FUN_00019ba8(local_60);
                              local_60 = (code *)0x0;
                              local_60 = (code *)(*(code *)PTR_PyNumber_Add_00052500)
                                                           (local_58[0],local_30);
                              if (local_60 == (code *)0x0) {
                                uVar12 = 0x1c7a;
                                local_60 = (code *)0x0;
                                local_50 = (code *)0x0;
                              }
                              else {
                                FUN_00019ba8(local_58[0]);
                                local_58[0] = (int *)0x0;
                                if (((undefined *)local_5c[1] == puVar2) &&
                                   (local_58[0] = (int *)local_5c[3], local_58[0] != (int *)0x0)) {
                                  local_5c = (int *)local_5c[2];
                                  *local_58[0] = *local_58[0] + 1;
                                  *local_5c = *local_5c + 1;
                                  FUN_00019ba8();
                                  if (local_58[0] == (int *)0x0) goto LAB_00035714;
                                  local_70 = (int *)FUN_0001e58c();
                                }
                                else {
LAB_00035714:
                                  local_70 = (int *)FUN_0001e790(local_5c,local_60);
                                }
                                FUN_0001a404(local_58[0]);
                                local_58[0] = (int *)0x0;
                                FUN_00019ba8(local_60);
                                local_60 = (code *)0x0;
                                if (local_70 != (int *)0x0) {
                                  FUN_00019ba8(local_5c);
                                  piVar14 = local_70;
                                  local_5c = (int *)0x0;
                                  bVar1 = local_70 != (int *)PTR__Py_NoneStruct_000523c8;
                                  local_70 = (int *)0x0;
                                  if (bVar1) {
LAB_00035288:
                                    pcVar4 = (code *)0x0;
                                    iVar5 = *piVar14;
LAB_0003528c:
                                    piVar15 = (int *)0x0;
                                    *piVar14 = iVar5 + 1;
                                    piVar13 = piVar14;
                                    goto LAB_00034b98;
                                  }
                                  iVar5 = (*(code *)PTR__PyThreadState_UncheckedGet_00052510)();
                                  (*local_38)(iVar5,&local_6c,local_40,local_3c);
                                  local_5c = (int *)(*local_50)(local_4c,*(undefined4 *)
                                                                          (local_34 + 0x2b90));
                                  if (local_5c == (int *)0x0) {
                                    uVar12 = 0x1cb2;
                                  }
                                  else {
                                    local_60 = (code *)(*local_50)(local_5c,*(undefined4 *)
                                                                             (PTR_DAT_0005229c +
                                                                             0x2c2c));
                                    if (local_60 == (code *)0x0) {
                                      uVar12 = 0x1cb4;
                                    }
                                    else {
                                      FUN_00019ba8(local_5c);
                                      local_5c = (int *)0x0;
                                      if ((*(undefined **)(local_60 + 4) == puVar2) &&
                                         (local_5c = *(int **)(local_60 + 0xc),
                                         local_5c != (int *)0x0)) {
                                        local_60 = *(code **)(local_60 + 8);
                                        *local_5c = *local_5c + 1;
                                        *(int *)local_60 = *(int *)local_60 + 1;
                                        FUN_00019ba8();
                                        if (local_5c == (int *)0x0) goto LAB_000352bc;
                                        local_70 = (int *)FUN_0001e58c(local_60,local_5c,local_48);
                                      }
                                      else {
LAB_000352bc:
                                        local_70 = (int *)FUN_0001e790(local_60,local_48);
                                      }
                                      FUN_0001a404(local_5c);
                                      local_5c = (int *)0x0;
                                      if (local_70 != (int *)0x0) {
                                        FUN_00019ba8(local_60);
                                        local_60 = (code *)0x0;
                                        FUN_00019ba8(local_70);
                                        local_70 = (int *)0x0;
                                        FUN_0001a404(local_6c);
                                        local_6c = 0;
                                        FUN_0001a404(local_68);
                                        local_68 = 0;
                                        FUN_0001a404(local_64);
                                        local_64 = 0;
                                        goto LAB_00035288;
                                      }
                                      uVar12 = 0x1cc3;
                                    }
                                  }
                                  FUN_0001a404(local_58[0]);
                                  local_58[0] = (int *)0x0;
                                  FUN_0001a404(local_70);
                                  local_70 = (int *)0x0;
                                  FUN_0001a404(local_5c);
                                  local_5c = (int *)0x0;
                                  FUN_0001a404(local_60);
                                  local_60 = (code *)0x0;
                                  FUN_0001a404(0);
                                  iVar10 = FUN_000194a0(*(undefined4 *)(iVar5 + 0x34),
                                                        *(undefined4 *)PTR_PyExc_Exception_00052494)
                                  ;
                                  local_4c = (code *)(PTR_LAB_000522a8 + -0x4800);
                                  if (iVar10 == 0) {
                                    uVar8 = 0xaf;
LAB_00035584:
                                    piVar6 = (int *)0x0;
                                    pcVar7 = (code *)0x0;
                                    pcVar4 = (code *)0x0;
                                  }
                                  else {
                                    FUN_0001ac3c(PTR_DAT_000522ac + -0x1d30,uVar12,0xaf,
                                                 PTR_DAT_000522ac + -0x2380);
                                    iVar10 = FUN_0001a42c(iVar5,&local_70,&local_60,&local_5c);
                                    pcVar4 = local_60;
                                    puVar11 = PTR_DAT_0005229c;
                                    if (iVar10 < 0) {
                                      uVar12 = 0x1ce6;
                                      uVar8 = 0xb0;
                                      goto LAB_00035584;
                                    }
                                    *(int *)local_60 = *(int *)local_60 + 1;
                                    if ((*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac) + 0x10) ==
                                         *(int *)(PTR_DAT_0005229c + 0x2728)) &&
                                       (*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac) + 0x14) ==
                                        *(int *)(PTR_DAT_0005229c + 0x272c))) {
                                      pcVar7 = *(code **)(puVar11 + 0x2720);
                                      if (pcVar7 == (code *)0x0) {
                                        pcVar7 = (code *)FUN_0001964c(*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2cb0));
                                        goto LAB_00035528;
                                      }
                                      *(int *)pcVar7 = *(int *)pcVar7 + 1;
LAB_000353f4:
                                      local_48 = pcVar7;
                                      piVar6 = (int *)(*local_50)(pcVar7,*(undefined4 *)
                                                                          (PTR_DAT_0005229c + 0x2ad0
                                                                          ));
                                      if (piVar6 == (int *)0x0) {
                                        uVar12 = 0x1cf6;
                                        pcVar7 = local_48;
                                      }
                                      else {
                                        FUN_00019ba8(local_48);
                                        if (((undefined *)piVar6[1] == puVar2) &&
                                           (piVar15 = (int *)piVar6[3], piVar15 != (int *)0x0)) {
                                          piVar13 = (int *)piVar6[2];
                                          *piVar15 = *piVar15 + 1;
                                          *piVar13 = *piVar13 + 1;
                                          FUN_00019ba8(piVar6);
                                          local_58[0] = (int *)FUN_0001e58c(piVar13,piVar15,pcVar4);
                                          piVar6 = piVar13;
                                        }
                                        else {
                                          local_58[0] = (int *)FUN_0001e790(piVar6,pcVar4);
                                          piVar15 = (int *)0x0;
                                        }
                                        FUN_0001a404(piVar15);
                                        if (local_58[0] != (int *)0x0) {
                                          FUN_00019ba8(piVar6);
                                          FUN_00019ba8(local_58[0]);
                                          local_58[0] = (int *)0x0;
                                          FUN_0001a404(local_70);
                                          local_70 = (int *)0x0;
                                          FUN_0001a404(local_60);
                                          local_60 = (code *)0x0;
                                          FUN_0001a404(local_5c);
                                          local_5c = (int *)0x0;
                                          (*local_4c)(*(undefined4 *)(iVar5 + 0x50),local_6c,
                                                      local_68,local_64);
                                          iVar5 = *piVar14;
                                          goto LAB_0003528c;
                                        }
                                        uVar12 = 0x1d05;
                                        pcVar7 = (code *)0x0;
                                      }
                                    }
                                    else {
                                      pcVar7 = (code *)FUN_000196cc(*(undefined4 *)
                                                                     (PTR_DAT_0005229c + 0x2cb0),
                                                                    PTR_DAT_0005229c + 0x2728,
                                                                    puVar11 + 0x2720);
LAB_00035528:
                                      if (pcVar7 != (code *)0x0) goto LAB_000353f4;
                                      piVar6 = (int *)0x0;
                                      uVar12 = 0x1cf4;
                                    }
                                    uVar8 = 0xb1;
                                  }
                                  piVar15 = (int *)0x0;
                                  local_50 = pcVar7;
                                  (*local_4c)(*(undefined4 *)(iVar5 + 0x50),local_6c,local_68,
                                              local_64);
                                  piVar13 = (int *)PTR__Py_NoneStruct_000523c8;
                                  goto LAB_00034eb4;
                                }
                                uVar12 = 0x1c8a;
                                local_50 = (code *)0x0;
                              }
                            }
                          }
                        }
                      }
                      piVar15 = (int *)0x0;
                      pcVar4 = (code *)0x0;
                      piVar6 = (int *)0x0;
                      uVar8 = 0xac;
                      piVar13 = (int *)0x0;
                      goto LAB_00034eb4;
                    }
                    uVar12 = 0x1bb1;
                    local_58[0] = (int *)0x0;
                  }
                  else if (((undefined *)local_5c[1] == PTR_PyCFunction_Type_00052300) &&
                          ((*(uint *)(local_5c[2] + 8) & 0xffffff8d) == 0x80)) {
                    local_7c[0] = local_60;
                    local_7c[1] = pcVar4;
                    local_74 = iVar5;
                    local_58[0] = (int *)FUN_0001838c(local_5c,local_7c + -iVar10);
                    if (local_58[0] != (int *)0x0) goto LAB_00034c80;
                    uVar12 = 0x1bbb;
                    local_58[0] = (int *)0x0;
                  }
                  else {
                    local_70 = (int *)(*(code *)PTR_PyTuple_New_00052414)(iVar10 + 3);
                    if (local_70 == (int *)0x0) {
                      uVar12 = 0x1bc3;
                    }
                    else {
                      if (piVar15 != (int *)0x0) {
                        local_70[3] = (int)piVar15;
                      }
                      local_70[iVar10 + 3] = (int)local_60;
                      *(int *)pcVar4 = *(int *)pcVar4 + 1;
                      local_70[iVar10 + 5] = iVar5;
                      local_70[iVar10 + 4] = (int)pcVar4;
                      local_60 = (code *)0x0;
                      local_58[0] = (int *)FUN_000189e4(local_5c,local_70,0);
                      if (local_58[0] != (int *)0x0) {
                        FUN_00019ba8(local_70);
                        local_70 = (int *)0x0;
                        goto LAB_00034ca8;
                      }
                      piVar15 = (int *)0x0;
                      uVar12 = 0x1bd1;
                      iVar5 = 0;
                      local_58[0] = (int *)0x0;
                    }
                  }
                }
              }
            }
          }
        }
        FUN_0001a404(local_58[0]);
        local_58[0] = (int *)0x0;
        FUN_0001a404(local_70);
        local_70 = (int *)0x0;
        FUN_0001a404(local_5c);
        local_5c = (int *)0x0;
        FUN_0001a404(local_60);
        local_60 = (code *)0x0;
        FUN_0001a404(iVar5);
        FUN_0001a404(piVar15);
        iVar5 = FUN_000194a0(*(int *)(local_44 + 0x34),*(undefined4 *)PTR_PyExc_Exception_00052494);
        if (iVar5 == 0) {
          uVar8 = 0xa7;
LAB_00034e84:
          piVar6 = (int *)0x0;
          piVar15 = (int *)0x0;
        }
        else {
          FUN_0001ac3c(PTR_DAT_000522ac + -0x1d30,uVar12,0xa7,PTR_DAT_000522ac + -0x2380);
          iVar5 = FUN_0001a42c(local_44,local_58,&local_5c,&local_70);
          piVar15 = local_5c;
          puVar11 = PTR_DAT_0005229c;
          if (iVar5 < 0) {
            uVar12 = 0x1bf6;
            uVar8 = 0xa8;
            goto LAB_00034e84;
          }
          *local_5c = *local_5c + 1;
          if ((*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac) + 0x10) ==
               *(int *)(PTR_DAT_0005229c + 0x2738)) &&
             (*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac) + 0x14) ==
              *(int *)(PTR_DAT_0005229c + 0x273c))) {
            pcVar4 = *(code **)(puVar11 + 0x2730);
            if (pcVar4 == (code *)0x0) {
              pcVar4 = (code *)FUN_0001964c(*(undefined4 *)(PTR_DAT_0005229c + 0x2cb0));
            }
            else {
              *(int *)pcVar4 = *(int *)pcVar4 + 1;
            }
          }
          else {
            pcVar4 = (code *)FUN_000196cc(*(undefined4 *)(PTR_DAT_0005229c + 0x2cb0),
                                          PTR_DAT_0005229c + 0x2738,puVar11 + 0x2730);
          }
          local_60 = pcVar4;
          if (pcVar4 == (code *)0x0) {
            uVar12 = 0x1c04;
            piVar6 = (int *)0x0;
LAB_00034f48:
            uVar8 = 0xa9;
          }
          else {
            piVar6 = (int *)(*local_50)(pcVar4,*(undefined4 *)(PTR_DAT_0005229c + 0x2d88));
            if (piVar6 == (int *)0x0) {
              uVar12 = 0x1c06;
              goto LAB_00034f48;
            }
            FUN_00019ba8(local_60);
            local_60 = (code *)0x0;
            piVar13 = piVar6;
            if (((undefined *)piVar6[1] == puVar2) &&
               (local_60 = (code *)piVar6[3], local_60 != (code *)0x0)) {
              piVar13 = (int *)piVar6[2];
              *(int *)local_60 = *(int *)local_60 + 1;
              *piVar13 = *piVar13 + 1;
              FUN_00019ba8(piVar6);
            }
            if (local_60 == (code *)0x0) {
              iVar5 = FUN_0001e790(piVar13,piVar15);
            }
            else {
              iVar5 = FUN_0001e58c(piVar13,local_60,piVar15);
            }
            FUN_0001a404(local_60);
            local_60 = (code *)0x0;
            if (iVar5 == 0) {
              uVar12 = 0x1c15;
              piVar6 = piVar13;
              goto LAB_00034f48;
            }
            FUN_00019ba8(piVar13);
            FUN_00019ba8(iVar5);
            piVar6 = (int *)(*local_50)(local_4c,*(undefined4 *)(local_34 + 0x2b90));
            if (piVar6 == (int *)0x0) {
              uVar12 = 0x1c21;
            }
            else {
              local_60 = (code *)(*local_50)(piVar6,*(undefined4 *)(PTR_DAT_0005229c + 0x2c2c));
              if (local_60 == (code *)0x0) {
                uVar12 = 0x1c23;
              }
              else {
                FUN_00019ba8(piVar6);
                if ((*(undefined **)(local_60 + 4) == puVar2) &&
                   (piVar6 = *(int **)(local_60 + 0xc), piVar6 != (int *)0x0)) {
                  local_60 = *(code **)(local_60 + 8);
                  *piVar6 = *piVar6 + 1;
                  *(int *)local_60 = *(int *)local_60 + 1;
                  FUN_00019ba8();
                  iVar5 = FUN_0001e58c(local_60,piVar6,local_48);
                }
                else {
                  piVar6 = (int *)0x0;
                  iVar5 = FUN_0001e790(local_60,local_48);
                }
                FUN_0001a404(piVar6);
                uVar12 = 0x1c32;
                piVar6 = (int *)0x0;
                if (iVar5 != 0) {
                  pcVar4 = (code *)0x0;
                  FUN_00019ba8(local_60);
                  local_60 = (code *)0x0;
                  FUN_00019ba8(iVar5);
                  piVar14 = (int *)PTR__Py_NoneStruct_000523c8;
                  *(int *)PTR__Py_NoneStruct_000523c8 = *(int *)PTR__Py_NoneStruct_000523c8 + 1;
                  FUN_00019ba8(local_58[0]);
                  local_58[0] = (int *)0x0;
                  FUN_00019ba8(local_5c);
                  local_5c = (int *)0x0;
                  FUN_00019ba8(local_70);
                  local_70 = (int *)0x0;
                  FUN_0001b800(*(int *)(local_44 + 0x50),local_64,local_68,local_6c);
                  piVar13 = (int *)0x0;
                  goto LAB_00034b98;
                }
              }
            }
            uVar8 = 0xaa;
          }
        }
        pcVar4 = (code *)0x0;
        FUN_0001b800(*(int *)(local_44 + 0x50),local_64,local_68,local_6c);
        local_50 = (code *)0x0;
        piVar13 = (int *)0x0;
      }
    }
  }
LAB_00034eb4:
  FUN_0001a404(local_58[0]);
  FUN_0001a404(local_5c);
  FUN_0001a404(local_60);
  FUN_0001a404(local_50);
  FUN_0001a404(piVar6);
  FUN_0001a404(local_70);
  piVar14 = (int *)0x0;
  FUN_0001ac3c(PTR_DAT_000522ac + -0x1d30,uVar12,uVar8,PTR_DAT_000522ac + -0x2380);
LAB_00034b98:
  FUN_0001a404(piVar3);
  FUN_0001a404(piVar15);
  FUN_0001a404(piVar13);
  FUN_0001a404(pcVar4);
  return piVar14;
}


