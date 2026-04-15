FUNCTION FUN_0002bac4 @ 0002bac4


int * FUN_0002bac4(undefined4 param_1,int param_2,int param_3)

{
  int *in_v0;
  int *piVar1;
  int iVar2;
  int *piVar3;
  code *pcVar4;
  int iVar5;
  uint uVar6;
  undefined *puVar7;
  uint uVar8;
  int iVar9;
  int *piVar10;
  undefined *puVar11;
  code *pcVar12;
  int *piVar13;
  uint uVar14;
  int *piVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  code *pcVar18;
  code *pcVar19;
  code *pcVar20;
  int *piVar21;
  int *piVar22;
  int *piVar23;
  undefined *puVar24;
  code *local_ec;
  int *local_e8;
  int *local_e4;
  int *local_e0;
  int *local_dc;
  int local_d8;
  undefined4 local_d4;
  undefined4 local_d0;
  int *local_cc;
  int *local_c8;
  int *local_c4;
  code *local_c0;
  int *local_bc;
  int *local_b8;
  int *local_b4;
  code *local_b0;
  int *local_ac;
  int *local_a8;
  code *local_a4;
  undefined4 local_a0;
  code *local_9c;
  code *local_98;
  int *local_94;
  code *local_90;
  int *local_8c;
  code *local_88;
  code *local_84;
  int local_80;
  undefined *local_7c;
  int *local_78;
  int local_74;
  int local_70;
  code *local_6c;
  int *local_68;
  code *local_64;
  code *local_60;
  undefined *local_5c;
  undefined *local_58;
  undefined *local_54;
  undefined *local_50;
  undefined *local_4c;
  int local_48;
  int local_44;
  undefined *local_40;
  undefined *local_3c;
  undefined *local_38;
  undefined *local_34;
  undefined *local_30;
  
  local_ec = (code *)0x0;
  local_e8 = (int *)0x0;
  uVar14 = *(uint *)(param_2 + 8);
  if (param_3 != 0) {
    if (uVar14 < 5) {
                    /* WARNING: Could not emulate address calculation at 0x0002bb24 */
                    /* WARNING: Treating indirect jump as call */
      piVar1 = (int *)(*(code *)(&_gp_1 + *(int *)(PTR_DAT_000522ac + uVar14 * 4 + -0x14c0)))();
      return piVar1;
    }
switchD_0002bb30_default:
    FUN_0001859c(PTR_DAT_000522ac + -0x1fa4,0,3,4,*(undefined4 *)(param_2 + 8));
    FUN_0001ac3c(PTR_DAT_000522ac + -0x1f88,0x3274,0x14f,PTR_DAT_000522ac + -0x2380);
    return (int *)0x0;
  }
  local_e4 = in_v0;
  if (uVar14 != 3) {
    if (uVar14 != 4) goto switchD_0002bb30_default;
    local_e4 = *(int **)(param_2 + 0x18);
  }
  local_e8 = *(int **)(param_2 + 0x14);
  local_ec = *(code **)(param_2 + 0x10);
  local_a0 = *(undefined4 *)(param_2 + 0xc);
  local_c4 = (int *)0x0;
  local_c8 = (int *)0x0;
  local_cc = (int *)0x0;
  local_d0 = 0;
  local_d4 = 0;
  local_d8 = 0;
  local_78 = local_e4;
  local_b0 = local_ec;
  local_ac = local_e8;
  local_94 = (int *)FUN_000197c0(*(undefined4 *)(PTR_DAT_0005229c + 0x2f70),
                                 *(undefined4 *)(PTR_DAT_0005229c + 0x2fa0),0);
  local_84 = (code *)(PTR_LAB_000522a8 + -0x6458);
  local_90 = (code *)(PTR_LAB_000522a8 + -0x5bfc);
  piVar1 = (int *)PTR__Py_NoneStruct_000523c8;
  if (local_94 == (int *)0x0) {
    uVar17 = 0x3352;
    uVar16 = 0x14f;
    piVar22 = (int *)0x0;
    *(int *)PTR__Py_NoneStruct_000523c8 = *(int *)PTR__Py_NoneStruct_000523c8 + 1;
    piVar21 = (int *)0x0;
    local_b8 = (int *)0x0;
    local_bc = (int *)0x0;
    piVar15 = (int *)0x0;
    piVar10 = (int *)0x0;
    local_b4 = (int *)0x0;
    local_a8 = (int *)0x0;
    local_8c = (int *)0x0;
    piVar13 = (int *)0x0;
    piVar3 = (int *)0x0;
    piVar23 = local_c4;
    local_94 = piVar1;
  }
  else {
    local_c4 = (int *)(*(code *)PTR_PySet_New_00052534)(0);
    local_8c = local_c4;
    if (local_c4 == (int *)0x0) {
      piVar3 = (int *)0x0;
      piVar22 = (int *)0x0;
      piVar21 = (int *)0x0;
      piVar13 = (int *)0x0;
      local_b8 = (int *)0x0;
      local_bc = (int *)0x0;
      piVar15 = (int *)0x0;
      piVar10 = (int *)0x0;
      local_b4 = (int *)0x0;
      local_a8 = (int *)0x0;
      uVar17 = 0x335e;
      uVar16 = 0x150;
      piVar23 = local_c4;
    }
    else {
      iVar2 = (*(code *)PTR_PySet_Add_00052354)(local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2a94))
      ;
      puVar11 = PTR_DAT_0005229c;
      if (iVar2 < 0) {
        uVar17 = 0x3360;
        uVar16 = 0x150;
        piVar3 = (int *)0x0;
        piVar22 = (int *)0x0;
        piVar21 = (int *)0x0;
        piVar13 = (int *)0x0;
        local_b8 = (int *)0x0;
        local_bc = (int *)0x0;
        piVar15 = (int *)0x0;
        piVar10 = (int *)0x0;
        local_b4 = (int *)0x0;
        local_a8 = (int *)0x0;
        local_8c = (int *)0x0;
        piVar23 = local_c4;
      }
      else {
        iVar2 = (*(code *)PTR_PySet_Add_00052354)
                          (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2a7c));
        if (iVar2 < 0) {
          uVar17 = 0x3361;
          uVar16 = 0x150;
          piVar3 = (int *)0x0;
          piVar22 = (int *)0x0;
          piVar21 = (int *)0x0;
          piVar13 = (int *)0x0;
          local_b8 = (int *)0x0;
          local_bc = (int *)0x0;
          piVar15 = (int *)0x0;
          piVar10 = (int *)0x0;
          local_b4 = (int *)0x0;
          local_a8 = (int *)0x0;
          local_8c = (int *)0x0;
          piVar23 = local_c4;
        }
        else {
          iVar2 = (*(code *)PTR_PySet_Add_00052354)
                            (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2a78));
          if (iVar2 < 0) {
            uVar17 = 0x3362;
            uVar16 = 0x150;
            piVar3 = (int *)0x0;
            piVar22 = (int *)0x0;
            piVar21 = (int *)0x0;
            piVar13 = (int *)0x0;
            local_b8 = (int *)0x0;
            local_bc = (int *)0x0;
            piVar15 = (int *)0x0;
            piVar10 = (int *)0x0;
            local_b4 = (int *)0x0;
            local_a8 = (int *)0x0;
            local_8c = (int *)0x0;
            piVar23 = local_c4;
          }
          else {
            iVar2 = (*(code *)PTR_PySet_Add_00052354)
                              (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2a74));
            if (iVar2 < 0) {
              uVar17 = 0x3363;
              uVar16 = 0x150;
              piVar3 = (int *)0x0;
              piVar22 = (int *)0x0;
              piVar21 = (int *)0x0;
              piVar13 = (int *)0x0;
              local_b8 = (int *)0x0;
              local_bc = (int *)0x0;
              piVar15 = (int *)0x0;
              piVar10 = (int *)0x0;
              local_b4 = (int *)0x0;
              local_a8 = (int *)0x0;
              local_8c = (int *)0x0;
              piVar23 = local_c4;
            }
            else {
              iVar2 = (*(code *)PTR_PySet_Add_00052354)
                                (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2a70));
              if (iVar2 < 0) {
                uVar17 = 0x3364;
                uVar16 = 0x150;
                piVar3 = (int *)0x0;
                piVar22 = (int *)0x0;
                piVar21 = (int *)0x0;
                piVar13 = (int *)0x0;
                local_b8 = (int *)0x0;
                local_bc = (int *)0x0;
                piVar15 = (int *)0x0;
                piVar10 = (int *)0x0;
                local_b4 = (int *)0x0;
                local_a8 = (int *)0x0;
                local_8c = (int *)0x0;
                piVar23 = local_c4;
              }
              else {
                iVar2 = (*(code *)PTR_PySet_Add_00052354)
                                  (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2a90));
                local_8c = local_c4;
                if (iVar2 < 0) {
                  uVar17 = 0x3365;
                  uVar16 = 0x150;
                  piVar3 = (int *)0x0;
                  piVar22 = (int *)0x0;
                  piVar21 = (int *)0x0;
                  piVar13 = (int *)0x0;
                  local_b8 = (int *)0x0;
                  local_bc = (int *)0x0;
                  piVar15 = (int *)0x0;
                  piVar10 = (int *)0x0;
                  local_b4 = (int *)0x0;
                  local_a8 = (int *)0x0;
                  local_8c = (int *)0x0;
                  piVar23 = local_c4;
                }
                else {
                  local_c4 = (int *)0x0;
                  local_c4 = (int *)(*(code *)PTR__PyDict_NewPresized_000522fc)(10);
                  local_a8 = local_c4;
                  if (local_c4 == (int *)0x0) {
                    piVar3 = (int *)0x0;
                    piVar22 = (int *)0x0;
                    piVar21 = (int *)0x0;
                    piVar13 = (int *)0x0;
                    local_b8 = (int *)0x0;
                    local_bc = (int *)0x0;
                    piVar15 = (int *)0x0;
                    piVar10 = (int *)0x0;
                    local_b4 = (int *)0x0;
                    uVar17 = 0x3370;
                    uVar16 = 0x152;
                    piVar23 = local_c4;
                  }
                  else {
                    iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                      (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2d1c),
                                       *(undefined4 *)(PTR_DAT_0005229c + 0x2aac));
                    if (iVar2 < 0) {
                      uVar17 = 0x3372;
                      uVar16 = 0x152;
                      piVar3 = (int *)0x0;
                      piVar22 = (int *)0x0;
                      piVar21 = (int *)0x0;
                      piVar13 = (int *)0x0;
                      local_b8 = (int *)0x0;
                      local_bc = (int *)0x0;
                      piVar15 = (int *)0x0;
                      piVar10 = (int *)0x0;
                      local_b4 = (int *)0x0;
                      local_a8 = (int *)0x0;
                      piVar23 = local_c4;
                    }
                    else {
                      iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                        (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2d28),
                                         *(undefined4 *)(PTR_DAT_0005229c + 0x2aa8));
                      if (iVar2 < 0) {
                        uVar17 = 0x3373;
                        uVar16 = 0x152;
                        piVar3 = (int *)0x0;
                        piVar22 = (int *)0x0;
                        piVar21 = (int *)0x0;
                        piVar13 = (int *)0x0;
                        local_b8 = (int *)0x0;
                        local_bc = (int *)0x0;
                        piVar15 = (int *)0x0;
                        piVar10 = (int *)0x0;
                        local_b4 = (int *)0x0;
                        local_a8 = (int *)0x0;
                        piVar23 = local_c4;
                      }
                      else {
                        iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                          (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2b44),
                                           *(undefined4 *)(PTR_DAT_0005229c + 0x2aa4));
                        if (iVar2 < 0) {
                          uVar17 = 0x3374;
                          uVar16 = 0x152;
                          piVar3 = (int *)0x0;
                          piVar22 = (int *)0x0;
                          piVar21 = (int *)0x0;
                          piVar13 = (int *)0x0;
                          local_b8 = (int *)0x0;
                          local_bc = (int *)0x0;
                          piVar15 = (int *)0x0;
                          piVar10 = (int *)0x0;
                          local_b4 = (int *)0x0;
                          local_a8 = (int *)0x0;
                          piVar23 = local_c4;
                        }
                        else {
                          iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                            (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2d44),
                                             *(undefined4 *)(PTR_DAT_0005229c + 0x2aa0));
                          if (iVar2 < 0) {
                            uVar17 = 0x3375;
                            uVar16 = 0x152;
                            piVar3 = (int *)0x0;
                            piVar22 = (int *)0x0;
                            piVar21 = (int *)0x0;
                            piVar13 = (int *)0x0;
                            local_b8 = (int *)0x0;
                            local_bc = (int *)0x0;
                            piVar15 = (int *)0x0;
                            piVar10 = (int *)0x0;
                            local_b4 = (int *)0x0;
                            local_a8 = (int *)0x0;
                            piVar23 = local_c4;
                          }
                          else {
                            iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                              (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2d38),
                                               *(undefined4 *)(PTR_DAT_0005229c + 0x2a9c));
                            if (iVar2 < 0) {
                              uVar17 = 0x3376;
                              uVar16 = 0x152;
                              piVar3 = (int *)0x0;
                              piVar22 = (int *)0x0;
                              piVar21 = (int *)0x0;
                              piVar13 = (int *)0x0;
                              local_b8 = (int *)0x0;
                              local_bc = (int *)0x0;
                              piVar15 = (int *)0x0;
                              piVar10 = (int *)0x0;
                              local_b4 = (int *)0x0;
                              local_a8 = (int *)0x0;
                              piVar23 = local_c4;
                            }
                            else {
                              iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                                (local_c4,*(undefined4 *)(PTR_DAT_0005229c + 0x2b40)
                                                 ,*(undefined4 *)(PTR_DAT_0005229c + 0x2a98));
                              if (iVar2 < 0) {
                                uVar17 = 0x3377;
                                uVar16 = 0x152;
                                piVar3 = (int *)0x0;
                                piVar22 = (int *)0x0;
                                piVar21 = (int *)0x0;
                                piVar13 = (int *)0x0;
                                local_b8 = (int *)0x0;
                                local_bc = (int *)0x0;
                                piVar15 = (int *)0x0;
                                piVar10 = (int *)0x0;
                                local_b4 = (int *)0x0;
                                local_a8 = (int *)0x0;
                                piVar23 = local_c4;
                              }
                              else {
                                iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                                  (local_c4,*(undefined4 *)
                                                             (PTR_DAT_0005229c + 0x2b3c),
                                                   *(undefined4 *)(PTR_DAT_0005229c + 0x2a8c));
                                if (iVar2 < 0) {
                                  uVar17 = 0x3378;
                                  uVar16 = 0x152;
                                  piVar3 = (int *)0x0;
                                  piVar22 = (int *)0x0;
                                  piVar21 = (int *)0x0;
                                  piVar13 = (int *)0x0;
                                  local_b8 = (int *)0x0;
                                  local_bc = (int *)0x0;
                                  piVar15 = (int *)0x0;
                                  piVar10 = (int *)0x0;
                                  local_b4 = (int *)0x0;
                                  local_a8 = (int *)0x0;
                                  piVar23 = local_c4;
                                }
                                else {
                                  iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                                    (local_c4,*(undefined4 *)
                                                               (PTR_DAT_0005229c + 0x2ca4),
                                                     *(undefined4 *)(PTR_DAT_0005229c + 0x2a88));
                                  if (iVar2 < 0) {
                                    uVar17 = 0x3379;
                                    uVar16 = 0x152;
                                    piVar3 = (int *)0x0;
                                    piVar22 = (int *)0x0;
                                    piVar21 = (int *)0x0;
                                    piVar13 = (int *)0x0;
                                    local_b8 = (int *)0x0;
                                    local_bc = (int *)0x0;
                                    piVar15 = (int *)0x0;
                                    piVar10 = (int *)0x0;
                                    local_b4 = (int *)0x0;
                                    local_a8 = (int *)0x0;
                                    piVar23 = local_c4;
                                  }
                                  else {
                                    iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                                      (local_c4,*(undefined4 *)
                                                                 (PTR_DAT_0005229c + 0x2d74),
                                                       *(undefined4 *)(PTR_DAT_0005229c + 0x2a84));
                                    if (iVar2 < 0) {
                                      uVar17 = 0x337a;
                                      uVar16 = 0x152;
                                      piVar3 = (int *)0x0;
                                      piVar22 = (int *)0x0;
                                      piVar21 = (int *)0x0;
                                      piVar13 = (int *)0x0;
                                      local_b8 = (int *)0x0;
                                      local_bc = (int *)0x0;
                                      piVar15 = (int *)0x0;
                                      piVar10 = (int *)0x0;
                                      local_b4 = (int *)0x0;
                                      local_a8 = (int *)0x0;
                                      piVar23 = local_c4;
                                    }
                                    else {
                                      iVar2 = (*(code *)PTR_PyDict_SetItem_00052360)
                                                        (local_c4,*(undefined4 *)
                                                                   (PTR_DAT_0005229c + 0x2bc0),
                                                         *(undefined4 *)(PTR_DAT_0005229c + 0x2a80))
                                      ;
                                      local_a8 = local_c4;
                                      if (iVar2 < 0) {
                                        uVar17 = 0x337b;
                                        uVar16 = 0x152;
                                        piVar3 = (int *)0x0;
                                        piVar22 = (int *)0x0;
                                        piVar21 = (int *)0x0;
                                        piVar13 = (int *)0x0;
                                        local_b8 = (int *)0x0;
                                        local_bc = (int *)0x0;
                                        piVar15 = (int *)0x0;
                                        piVar10 = (int *)0x0;
                                        local_b4 = (int *)0x0;
                                        local_a8 = (int *)0x0;
                                        piVar23 = local_c4;
                                      }
                                      else {
                                        local_58 = PTR_DAT_0005229c;
                                        local_c4 = (int *)0x0;
                                        if ((*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac) + 0x10) ==
                                             *(int *)(PTR_DAT_0005229c + 0x28e8)) &&
                                           (*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac) + 0x14) ==
                                            *(int *)(PTR_DAT_0005229c + 0x28ec))) {
                                          local_b4 = *(int **)(PTR_DAT_0005229c + 0x28e0);
                                          if (local_b4 == (int *)0x0) {
                                            local_b4 = (int *)FUN_0001964c(*(undefined4 *)
                                                                            (PTR_DAT_0005229c +
                                                                            0x2f54));
                                          }
                                          else {
                                            *local_b4 = *local_b4 + 1;
                                          }
                                        }
                                        else {
                                          local_b4 = (int *)FUN_000196cc(*(undefined4 *)
                                                                          (PTR_DAT_0005229c + 0x2f54
                                                                          ),PTR_DAT_0005229c +
                                                                            0x28e8,
                                                                         PTR_DAT_0005229c + 0x28e0);
                                        }
                                        puVar24 = PTR_DAT_0005229c;
                                        local_c4 = local_b4;
                                        if (local_b4 == (int *)0x0) {
                                          piVar3 = (int *)0x0;
                                          piVar22 = (int *)0x0;
                                          piVar21 = (int *)0x0;
                                          piVar13 = (int *)0x0;
                                          local_b8 = (int *)0x0;
                                          local_bc = (int *)0x0;
                                          piVar15 = (int *)0x0;
                                          piVar10 = (int *)0x0;
                                          uVar17 = 0x3386;
                                          uVar16 = 0x15d;
                                          piVar23 = local_c4;
                                        }
                                        else {
                                          local_c8 = (int *)FUN_00028a78(local_b4,*(undefined4 *)
                                                                                   (PTR_DAT_0005229c
                                                                                   + 0x2ab0),0);
                                          if (local_c8 == (int *)0x0) {
                                            piVar3 = (int *)0x0;
                                            piVar22 = (int *)0x0;
                                            piVar21 = (int *)0x0;
                                            piVar13 = (int *)0x0;
                                            local_b8 = (int *)0x0;
                                            local_bc = (int *)0x0;
                                            piVar15 = (int *)0x0;
                                            piVar10 = (int *)0x0;
                                            uVar17 = 0x3388;
                                            uVar16 = 0x15d;
                                            local_b4 = (int *)0x0;
                                            piVar23 = local_c4;
                                          }
                                          else {
                                            local_b4 = local_c8;
                                            (*local_84)(local_c4);
                                            local_c4 = (int *)0x0;
                                            local_c4 = (int *)FUN_0001ce3c(local_b0,local_c8);
                                            local_b4 = local_c4;
                                            if (local_c4 == (int *)0x0) {
                                              piVar3 = (int *)0x0;
                                              piVar22 = (int *)0x0;
                                              piVar21 = (int *)0x0;
                                              piVar13 = (int *)0x0;
                                              local_b8 = (int *)0x0;
                                              local_bc = (int *)0x0;
                                              piVar15 = (int *)0x0;
                                              piVar10 = (int *)0x0;
                                              uVar17 = 0x338b;
                                              uVar16 = 0x15d;
                                              piVar23 = (int *)0x0;
                                            }
                                            else {
                                              (*local_84)(local_c8);
                                              local_c8 = (int *)0x0;
                                              local_b4 = local_c4;
                                              local_c4 = (int *)0x0;
                                              if ((*(int *)(*(int *)(local_58 + 0x2fac) + 0x10) ==
                                                   *(int *)(PTR_DAT_0005229c + 0x28d8)) &&
                                                 (*(int *)(*(int *)(local_58 + 0x2fac) + 0x14) ==
                                                  *(int *)(PTR_DAT_0005229c + 0x28dc))) {
                                                piVar23 = *(int **)(PTR_DAT_0005229c + 0x28d0);
                                                if (piVar23 == (int *)0x0) {
                                                  piVar23 = (int *)FUN_0001964c(*(undefined4 *)
                                                                                 (PTR_DAT_0005229c +
                                                                                 0x2f44));
                                                }
                                                else {
                                                  *piVar23 = *piVar23 + 1;
                                                }
                                              }
                                              else {
                                                piVar23 = (int *)FUN_000196cc(*(undefined4 *)
                                                                               (PTR_DAT_0005229c +
                                                                               0x2f44),
                                                  PTR_DAT_0005229c + 0x28d8,
                                                  PTR_DAT_0005229c + 0x28d0);
                                              }
                                              if (piVar23 == (int *)0x0) {
                                                piVar3 = (int *)0x0;
                                                piVar22 = (int *)0x0;
                                                piVar21 = (int *)0x0;
                                                piVar13 = (int *)0x0;
                                                local_b8 = (int *)0x0;
                                                local_bc = (int *)0x0;
                                                piVar15 = (int *)0x0;
                                                uVar17 = 0x3398;
                                                uVar16 = 0x15e;
                                                piVar10 = (int *)0x0;
                                              }
                                              else {
                                                local_c4 = piVar23;
                                                local_c8 = (int *)FUN_00028a78(piVar23,*(undefined4
                                                                                         *)(puVar24 
                                                  + 0x2ab0),0);
                                                if (local_c8 == (int *)0x0) {
                                                  piVar3 = (int *)0x0;
                                                  piVar22 = (int *)0x0;
                                                  piVar21 = (int *)0x0;
                                                  piVar13 = (int *)0x0;
                                                  local_b8 = (int *)0x0;
                                                  local_bc = (int *)0x0;
                                                  piVar15 = (int *)0x0;
                                                  uVar17 = 0x339a;
                                                  uVar16 = 0x15e;
                                                  piVar10 = (int *)0x0;
                                                  piVar23 = local_c4;
                                                }
                                                else {
                                                  (*local_84)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  piVar10 = (int *)FUN_0001ce3c(local_b0,local_c8);
                                                  if (piVar10 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    local_bc = (int *)0x0;
                                                    piVar15 = (int *)0x0;
                                                    uVar17 = 0x339d;
                                                    uVar16 = 0x15e;
                                                    piVar23 = (int *)0x0;
                                                  }
                                                  else {
                                                    local_c4 = piVar10;
                                                    (*local_84)(local_c8);
                                                    piVar10 = local_c4;
                                                    local_c8 = (int *)0x0;
                                                    local_c4 = (int *)0x0;
                                                    local_c4 = (int *)(*(code *)
                                                  PTR_PyObject_RichCompare_000524c8)
                                                            (*(undefined4 *)
                                                              (PTR_DAT_0005229c + 0x2a6c),local_b4,1
                                                            );
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    local_bc = (int *)0x0;
                                                    uVar17 = 0x33aa;
                                                    uVar16 = 0x162;
                                                    piVar15 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    iVar2 = FUN_00018be8(local_c4);
                                                    if (iVar2 != 0) {
                                                      (*local_84)(local_c4);
                                                      local_c4 = (int *)(*(code *)
                                                  PTR_PyObject_RichCompare_000524c8)
                                                            (local_b4,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2a68),1
                                                            );
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    local_bc = (int *)0x0;
                                                    uVar17 = 0x33ad;
                                                    uVar16 = 0x162;
                                                    piVar15 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  iVar2 = FUN_00018be8(local_c4);
                                                  if (iVar2 < 0) {
                                                    uVar17 = 0x33af;
                                                    uVar16 = 0x162;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    local_bc = (int *)0x0;
                                                    piVar15 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    (*local_84)(local_c4);
                                                    local_c4 = (int *)0x0;
                                                    local_98 = (code *)(PTR_LAB_000522a8 + -0x6458);
                                                    if (iVar2 == 0) {
LAB_0002c4f4:
                                                      local_c4 = (int *)0x0;
                                                      local_c4 = (int *)FUN_0001e790(
                                                  PTR_PyUnicode_Type_0005233c,local_b4);
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    local_bc = (int *)0x0;
                                                    uVar17 = 0x33da;
                                                    uVar16 = 0x165;
                                                    piVar15 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    piVar15 = (int *)(*(code *)
                                                  PTR_PyNumber_Add_00052500)
                                                            (*(undefined4 *)
                                                              (PTR_DAT_0005229c + 0x2e54),local_c4);
                                                  if (piVar15 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    local_bc = (int *)0x0;
                                                    uVar17 = 0x33dc;
                                                    uVar16 = 0x165;
                                                    local_c8 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    local_c8 = piVar15;
                                                    (*local_98)(local_c4);
                                                    piVar15 = local_c8;
                                                    local_c8 = (int *)0x0;
LAB_0002c44c:
                                                    local_c4 = (int *)0x0;
                                                    local_60 = (code *)(PTR_LAB_000522a8 + -0x1870);
                                                    local_c8 = (int *)FUN_0001e790(
                                                  PTR_PyUnicode_Type_0005233c,piVar10);
                                                  if (local_c8 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    uVar17 = 0x33eb;
                                                    uVar16 = 0x166;
                                                    local_bc = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    local_bc = local_c8;
                                                    local_c4 = (int *)(*(code *)
                                                  PTR_PyNumber_Add_00052500)
                                                            (*(undefined4 *)
                                                              (PTR_DAT_0005229c + 0x2e00),local_c8);
                                                  local_bc = local_c4;
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    uVar17 = 0x33ed;
                                                    uVar16 = 0x166;
                                                    piVar23 = (int *)0x0;
                                                  }
                                                  else {
                                                    (*local_98)(local_c8);
                                                    piVar1 = local_c4;
                                                    local_c8 = (int *)0x0;
                                                    local_bc = local_c4;
                                                    local_c4 = (int *)0x0;
                                                    local_b8 = (int *)(*(code *)
                                                  PTR_PyNumber_Add_00052500)(piVar15,piVar1);
                                                  local_c4 = (int *)0x0;
                                                  if (local_b8 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x33fa;
                                                    uVar16 = 0x168;
                                                    piVar13 = (int *)0x0;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    local_c4 = (int *)FUN_0001c304(local_a8);
                                                    if (local_c4 == (int *)0x0) {
                                                      piVar3 = (int *)0x0;
                                                      piVar22 = (int *)0x0;
                                                      piVar21 = (int *)0x0;
                                                      uVar17 = 0x340f;
                                                      uVar16 = 0x16a;
                                                      piVar13 = (int *)0x0;
                                                      piVar23 = local_c4;
                                                    }
                                                    else {
                                                      iVar2 = FUN_00018b90(piVar10,local_c4,2);
                                                      if (iVar2 < 0) {
                                                        uVar17 = 0x3411;
                                                        uVar16 = 0x16a;
                                                        piVar3 = (int *)0x0;
                                                        piVar22 = (int *)0x0;
                                                        piVar21 = (int *)0x0;
                                                        piVar13 = (int *)0x0;
                                                        piVar23 = local_c4;
                                                      }
                                                      else {
                                                        (*local_98)(local_c4);
                                                        puVar11 = PTR__Py_NoneStruct_000523c8;
                                                        local_44 = 1;
                                                        if (iVar2 != 0) {
                                                          local_44 = 5;
                                                        }
                                                        local_68 = (int *)
                                                  PTR__Py_NoneStruct_000523c8;
                                                  local_c4 = (int *)0x0;
                                                  local_74 = 0;
                                                  *(int *)PTR__Py_NoneStruct_000523c8 =
                                                       *(int *)PTR__Py_NoneStruct_000523c8 + 1;
                                                  local_94[2] = (int)puVar11;
                                                  local_5c = PTR_DAT_0005229c;
                                                  local_30 = PTR_DAT_0005229c + 0x28c8;
                                                  local_64 = (code *)(PTR_LAB_000522a8 + -0x6314);
                                                  piVar13 = (int *)0x0;
                                                  do {
                                                    if ((*(int *)(*(int *)(local_58 + 0x2fac) + 0x10
                                                                 ) == *(int *)(local_5c + 0x28c8))
                                                       && (*(int *)(*(int *)(local_58 + 0x2fac) +
                                                                   0x14) ==
                                                           *(int *)(local_5c + 0x28cc))) {
                                                      piVar1 = *(int **)(PTR_DAT_0005229c + 0x28c0);
                                                      if (piVar1 == (int *)0x0) {
                                                        piVar1 = (int *)FUN_0001964c(*(undefined4 *)
                                                                                      (
                                                  PTR_DAT_0005229c + 0x2cb0));
                                                  }
                                                  else {
                                                    *piVar1 = *piVar1 + 1;
                                                  }
                                                  }
                                                  else {
                                                    piVar1 = (int *)FUN_000196cc(*(undefined4 *)
                                                                                  (PTR_DAT_0005229c
                                                                                  + 0x2cb0),local_30
                                                                                 ,PTR_DAT_0005229c +
                                                                                  0x28c0);
                                                  }
                                                  local_c8 = piVar1;
                                                  if (piVar1 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3446;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  puVar11 = PTR_DAT_0005229c;
                                                  local_9c = (code *)(PTR_LAB_000522a8 + -0x74a0);
                                                  local_cc = (int *)FUN_00018b60(piVar1,*(undefined4
                                                                                          *)(
                                                  PTR_DAT_0005229c + 0x2cfc));
                                                  local_40 = puVar11;
                                                  if (local_cc == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3448;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_98)(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  local_c8 = (int *)(*(code *)
                                                  PTR_PyTuple_New_00052414)(0xc);
                                                  puVar24 = PTR_PyUnicode_FromOrdinal_00052310;
                                                  puVar11 = PTR_DAT_000522ac;
                                                  if (local_c8 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x344b;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  piVar1 = *(int **)(PTR_DAT_0005229c + 0x2e64);
                                                  *piVar1 = *piVar1 + 1;
                                                  local_c8[3] = (int)piVar1;
                                                  iVar2 = (*(code *)puVar24)((int)(char)puVar11[
                                                  local_74 * 2 + -0x143b]);
                                                  puVar11 = PTR_DAT_0005229c;
                                                  if (iVar2 == 0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3453;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  local_a4 = *(code **)(iVar2 + 8);
                                                  local_c8[4] = iVar2;
                                                  piVar1 = *(int **)(puVar11 + 0x2df8);
                                                  *piVar1 = *piVar1 + 1;
                                                  local_c8[5] = (int)piVar1;
                                                  local_c0 = (code *)PTR_PyUnicode_Type_0005233c;
                                                  puVar11 = (undefined *)piVar10[1];
                                                  if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                    *piVar10 = *piVar10 + 1;
                                                    piVar1 = piVar10;
                                                  }
                                                  else {
                                                    if ((puVar11 == PTR_PyLong_Type_00052384) ||
                                                       (puVar11 == PTR_PyFloat_Type_00052520)) {
                                                      piVar1 = (int *)(**(code **)(puVar11 + 0x44))
                                                                                (piVar10);
                                                    }
                                                    else {
                                                      piVar1 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar10,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar1 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x345d;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  pcVar20 = (code *)0x7f;
                                                  if ((piVar1[4] & 0x40U) == 0) {
                                                    uVar14 = piVar1[4] & 0x1c;
                                                    pcVar20 = (code *)0xff;
                                                    if ((uVar14 != 4) &&
                                                       (pcVar20 = (code *)0xffff, uVar14 != 8)) {
                                                      pcVar20 = (code *)0x10ffff;
                                                    }
                                                  }
                                                  local_88 = (code *)piVar1[2];
                                                  local_3c = PTR_DAT_0005229c;
                                                  piVar21 = *(int **)(PTR_DAT_0005229c + 0x2dbc);
                                                  local_c8[6] = (int)piVar1;
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[7] = (int)piVar21;
                                                  puVar11 = *(undefined **)(local_b0 + 4);
                                                  if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                    *(int *)local_b0 = *(int *)local_b0 + 1;
                                                    pcVar18 = local_b0;
                                                  }
                                                  else {
                                                    if ((puVar11 == PTR_PyLong_Type_00052384) ||
                                                       (puVar11 == PTR_PyFloat_Type_00052520)) {
                                                      pcVar18 = (code *)(**(code **)(puVar11 + 0x44)
                                                                        )(local_b0);
                                                    }
                                                    else {
                                                      pcVar18 = (code *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_b0,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (pcVar18 == (code *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3468;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  puVar11 = PTR_DAT_0005229c;
                                                  local_c0 = (code *)0x7f;
                                                  if ((*(uint *)(pcVar18 + 0x10) & 0x40) == 0) {
                                                    uVar14 = *(uint *)(pcVar18 + 0x10) & 0x1c;
                                                    local_c0 = (code *)0xff;
                                                    if (uVar14 != 4) {
                                                      if (uVar14 == 8) {
                                                        local_c0 = (code *)0xffff;
                                                      }
                                                      else {
                                                        local_c0 = (code *)0x10ffff;
                                                      }
                                                    }
                                                  }
                                                  local_80 = *(int *)(pcVar18 + 8);
                                                  local_c8[8] = (int)pcVar18;
                                                  piVar1 = *(int **)(puVar11 + 11000);
                                                  *piVar1 = *piVar1 + 1;
                                                  local_c8[9] = (int)piVar1;
                                                  puVar11 = (undefined *)local_ac[1];
                                                  if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                    *local_ac = *local_ac + 1;
                                                    piVar1 = local_ac;
                                                  }
                                                  else {
                                                    if ((puVar11 == PTR_PyLong_Type_00052384) ||
                                                       (puVar11 == PTR_PyFloat_Type_00052520)) {
                                                      piVar1 = (int *)(**(code **)(puVar11 + 0x44))
                                                                                (local_ac);
                                                    }
                                                    else {
                                                      piVar1 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_ac,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar1 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3473;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  puVar11 = PTR_DAT_0005229c;
                                                  pcVar18 = (code *)0x7f;
                                                  if ((piVar1[4] & 0x40U) == 0) {
                                                    uVar14 = piVar1[4] & 0x1c;
                                                    pcVar18 = (code *)0xff;
                                                    if ((uVar14 != 4) &&
                                                       (pcVar18 = (code *)0xffff, uVar14 != 8)) {
                                                      pcVar18 = (code *)0x10ffff;
                                                    }
                                                  }
                                                  local_70 = piVar1[2];
                                                  piVar21 = *(int **)(PTR_DAT_0005229c + 0x2ce8);
                                                  local_c8[10] = (int)piVar1;
                                                  uVar16 = *(undefined4 *)(puVar11 + 0x2cf0);
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[0xb] = (int)piVar21;
                                                  piVar22 = (int *)(*local_9c)(local_a0,uVar16);
                                                  local_54 = puVar11;
                                                  local_38 = puVar11;
                                                  if (piVar22 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x347e;
                                                    uVar16 = 0x16e;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  puVar11 = (undefined *)piVar22[1];
                                                  if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                    *piVar22 = *piVar22 + 1;
                                                    piVar1 = piVar22;
                                                  }
                                                  else {
                                                    if ((puVar11 == PTR_PyLong_Type_00052384) ||
                                                       (puVar11 == PTR_PyFloat_Type_00052520)) {
                                                      piVar1 = (int *)(**(code **)(puVar11 + 0x44))
                                                                                (piVar22);
                                                    }
                                                    else {
                                                      piVar1 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar22,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar1 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x3480;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  pcVar12 = (code *)0x7f;
                                                  (*local_98)(piVar22);
                                                  if ((piVar1[4] & 0x40U) == 0) {
                                                    uVar14 = piVar1[4] & 0x1c;
                                                    pcVar12 = (code *)0xff;
                                                    if ((uVar14 != 4) &&
                                                       (pcVar12 = (code *)0xffff, uVar14 != 8)) {
                                                      pcVar12 = (code *)0x10ffff;
                                                    }
                                                  }
                                                  local_6c = (code *)piVar1[2];
                                                  puVar24 = PTR_DAT_0005229c;
                                                  piVar21 = *(int **)(PTR_DAT_0005229c + 0x2b50);
                                                  local_c8[0xc] = (int)piVar1;
                                                  puVar11 = PTR_DAT_0005229c;
                                                  uVar16 = *(undefined4 *)
                                                            (PTR_DAT_0005229c + 0x2b84);
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[0xd] = (int)piVar21;
                                                  piVar3 = (int *)(*local_9c)(local_a0,uVar16);
                                                  local_7c = puVar11;
                                                  local_34 = puVar24;
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x348c;
                                                    uVar16 = 0x16e;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  puVar11 = PTR_DAT_0005229c;
                                                  piVar22 = (int *)(*local_9c)(piVar3,*(undefined4 *
                                                                                       )(
                                                  PTR_DAT_0005229c + 0x2c04));
                                                  local_50 = puVar11;
                                                  if (piVar22 == (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x348e;
                                                    uVar16 = 0x16e;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_98)(piVar3);
                                                  puVar11 = (undefined *)piVar22[1];
                                                  if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                    *piVar22 = *piVar22 + 1;
                                                    piVar1 = piVar22;
                                                  }
                                                  else {
                                                    if ((puVar11 == PTR_PyLong_Type_00052384) ||
                                                       (puVar11 == PTR_PyFloat_Type_00052520)) {
                                                      piVar1 = (int *)(**(code **)(puVar11 + 0x44))
                                                                                (piVar22);
                                                    }
                                                    else {
                                                      piVar1 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar22,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar1 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x3491;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  (*local_98)(piVar22);
                                                  pcVar4 = (code *)0x7f;
                                                  if ((piVar1[4] & 0x40U) == 0) {
                                                    uVar14 = piVar1[4] & 0x1c;
                                                    pcVar4 = (code *)0xff;
                                                    if (uVar14 != 4) {
                                                      if (uVar14 == 8) {
                                                        pcVar4 = (code *)0xffff;
                                                      }
                                                      else {
                                                        pcVar4 = (code *)0x10ffff;
                                                      }
                                                    }
                                                  }
                                                  pcVar19 = local_c0;
                                                  if (local_c0 <= pcVar20) {
                                                    pcVar19 = pcVar20;
                                                  }
                                                  if (pcVar18 <= pcVar19) {
                                                    pcVar18 = pcVar19;
                                                  }
                                                  if (pcVar12 <= pcVar18) {
                                                    pcVar12 = pcVar18;
                                                  }
                                                  if (pcVar4 <= pcVar12) {
                                                    pcVar4 = pcVar12;
                                                  }
                                                  iVar2 = piVar1[2];
                                                  local_c8[0xe] = (int)piVar1;
                                                  iVar2 = (*local_64)(local_c8,0xc,
                                                                      local_a4 + 0x5b +
                                                                      (int)local_88 +
                                                                      local_70 + local_80 +
                                                                      (int)local_6c + iVar2,pcVar4);
                                                  if (iVar2 == 0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3499;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_98)(local_c8);
                                                  puVar11 = PTR_PyMethod_Type_00052528;
                                                  local_c8 = (int *)0x0;
                                                  if (((undefined *)local_cc[1] ==
                                                       PTR_PyMethod_Type_00052528) &&
                                                     (local_c8 = (int *)local_cc[3],
                                                     local_c8 != (int *)0x0)) {
                                                    local_cc = (int *)local_cc[2];
                                                    *local_c8 = *local_c8 + 1;
                                                    *local_cc = *local_cc + 1;
                                                    (*local_98)();
                                                    if (local_c8 == (int *)0x0) goto LAB_0002d5c4;
                                                    local_c4 = (int *)FUN_0001e58c(local_cc,local_c8
                                                                                   ,iVar2);
                                                  }
                                                  else {
LAB_0002d5c4:
                                                    local_c4 = (int *)(*local_60)(local_cc,iVar2);
                                                  }
                                                  local_a4 = (code *)(PTR_LAB_000522a8 + -0x5bfc);
                                                  FUN_0001a404(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  (*local_98)(iVar2);
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34a9;
                                                    uVar16 = 0x16e;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_98)(local_cc);
                                                  local_cc = (int *)0x0;
                                                  (*local_98)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  local_c4 = (int *)(*local_9c)(local_a0,*(
                                                  undefined4 *)(local_7c + 0x2b84));
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34b5;
                                                    uVar16 = 0x16f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  local_cc = (int *)(*local_9c)(local_c4,*(
                                                  undefined4 *)(local_54 + 0x2cf0));
                                                  if (local_cc == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34b7;
                                                    uVar16 = 0x16f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_98)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  local_6c = (code *)(PTR_LAB_000522a8 + -0x7418);
                                                  iVar2 = FUN_00018be8(local_cc);
                                                  if (iVar2 < 0) {
                                                    uVar17 = 0x34ba;
                                                    uVar16 = 0x16f;
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_98)(local_cc);
                                                  local_cc = (int *)0x0;
                                                  local_c0 = (code *)(PTR_LAB_000522a8 + -0x6458);
                                                  piVar1 = piVar13;
                                                  if (iVar2 != 0) {
                                                    local_cc = (int *)(*local_9c)(local_a0,*(
                                                  undefined4 *)(local_7c + 0x2b84));
                                                  if (local_cc == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34c1;
                                                    uVar16 = 0x16f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  local_c4 = (int *)(*local_9c)(local_cc,*(
                                                  undefined4 *)(local_50 + 0x2c04));
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34c3;
                                                    uVar16 = 0x16f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_98)(local_cc);
                                                  local_cc = (int *)0x0;
                                                  local_80 = (*local_6c)(local_c4);
                                                  if (local_80 < 0) {
                                                    uVar17 = 0x34c6;
                                                    uVar16 = 0x16f;
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_98)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  if (local_80 != 0) goto LAB_0002ebe4;
                                                  local_cc = (int *)(*local_9c)(local_a0,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2c0c));
                                                  if (local_cc == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34d4;
                                                    uVar16 = 0x170;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  piVar1 = (int *)(*local_9c)(local_cc,*(undefined4
                                                                                         *)(
                                                  PTR_DAT_0005229c + 0x2dd8));
                                                  if (piVar1 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34d6;
                                                    uVar16 = 0x170;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(local_cc);
                                                  local_cc = (int *)0x0;
                                                  piVar3 = piVar1;
                                                  if (((undefined *)piVar1[1] == puVar11) &&
                                                     (local_cc = (int *)piVar1[3],
                                                     local_cc != (int *)0x0)) {
                                                    piVar3 = (int *)piVar1[2];
                                                    *local_cc = *local_cc + 1;
                                                    *piVar3 = *piVar3 + 1;
                                                    (*local_c0)(piVar1);
                                                  }
                                                  if (local_cc == (int *)0x0) {
                                                    local_c4 = (int *)FUN_0001e6dc(piVar3);
                                                  }
                                                  else {
                                                    local_c4 = (int *)FUN_0001e790();
                                                  }
                                                  (*local_a4)(local_cc);
                                                  local_cc = (int *)0x0;
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x34e5;
                                                    uVar16 = 0x170;
                                                    piVar22 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(piVar3);
                                                  piVar1 = local_c4;
                                                  (*local_a4)(piVar13);
                                                  local_c4 = (int *)0x0;
                                                  local_c4 = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(local_7c + 0x2b84));
                                                  piVar13 = piVar1;
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34f3;
                                                    uVar16 = 0x171;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  piVar3 = (int *)FUN_00018b60(local_c4,*(undefined4
                                                                                          *)(
                                                  PTR_DAT_0005229c + 0x2c80));
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x34f5;
                                                    uVar16 = 0x171;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  iVar2 = FUN_00018cbc(piVar3,*(undefined4 *)
                                                                               (PTR_DAT_0005229c +
                                                                               0x2d7c));
                                                  if (iVar2 == 0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x34f8;
                                                    uVar16 = 0x171;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  piVar21 = (int *)FUN_00018cbc(piVar3,*(undefined4
                                                                                         *)(
                                                  PTR_DAT_0005229c + 0x2d98));
                                                  local_cc = piVar21;
                                                  if (piVar21 == (int *)0x0) {
                                                    uVar17 = 0x34fa;
                                                  }
                                                  else {
                                                    local_88 = (code *)PTR_PyMethod_Type_00052528;
                                                    local_c8 = (int *)0x0;
                                                    if (((undefined *)piVar21[1] ==
                                                         PTR_PyMethod_Type_00052528) &&
                                                       (local_c8 = (int *)piVar21[3],
                                                       local_c8 != (int *)0x0)) {
                                                      local_cc = (int *)piVar21[2];
                                                      *local_c8 = *local_c8 + 1;
                                                      *local_cc = *local_cc + 1;
                                                      (*local_c0)(piVar21);
                                                      if (local_c8 == (int *)0x0) goto LAB_00030944;
                                                      local_c4 = (int *)FUN_0001e790();
                                                    }
                                                    else {
LAB_00030944:
                                                      local_c4 = (int *)FUN_0001e6dc(local_cc);
                                                    }
                                                    (*local_a4)(local_c8);
                                                    local_c8 = (int *)0x0;
                                                    if (local_c4 != (int *)0x0) {
                                                      (*local_c0)(local_cc);
                                                      local_cc = (int *)0x0;
                                                      (*local_c0)(local_c4);
                                                      local_c4 = (int *)0x0;
                                                      (*local_c0)(piVar3);
                                                      local_70 = (*(code *)
                                                  PTR__PyThreadState_UncheckedGet_00052510)();
                                                  FUN_00018f78(local_70,&local_d0,&local_d4,
                                                               &local_d8);
                                                  piVar21 = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(local_7c + 0x2b84));
                                                  puVar11 = PTR_DAT_0005229c;
                                                  local_88 = (code *)(PTR_LAB_000522a8 + -0x6458);
                                                  local_4c = PTR_DAT_0005229c;
                                                  if (piVar21 == (int *)0x0) {
                                                    uVar16 = 0x351e;
LAB_0002d7a4:
                                                    local_4c = puVar11;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x172;
LAB_0002d7a8:
                                                    (*local_a4)(local_c4);
                                                    local_c4 = (int *)0x0;
                                                    (*local_a4)(piVar22);
                                                    (*local_a4)(piVar21);
                                                    (*local_a4)(local_c8);
                                                    local_c8 = (int *)0x0;
                                                    (*local_a4)(local_cc);
                                                    local_cc = (int *)0x0;
                                                    FUN_0001ac3c(PTR_DAT_000522ac + -0x1f88,uVar16,
                                                                 uVar17,PTR_DAT_000522ac + -0x2380);
                                                    iVar5 = FUN_0001a42c(local_70,&local_c4,
                                                                         &local_c8,&local_cc);
                                                    if (iVar5 < 0) {
                                                      uVar17 = 0x35b1;
                                                    }
                                                    else {
                                                      iVar5 = (*(code *)PTR_PyTuple_Pack_000522e4)
                                                                        (3,local_c4,local_c8,
                                                                         local_cc);
                                                      if (iVar5 == 0) {
                                                        uVar17 = 0x35b5;
                                                      }
                                                      else {
                                                        iVar9 = FUN_000189e4(iVar2,iVar5,0);
                                                        (*local_c0)(iVar2);
                                                        (*local_c0)(iVar5);
                                                        if (iVar9 == 0) {
                                                          uVar17 = 0x35ba;
                                                        }
                                                        else {
                                                          iVar2 = (*local_6c)(iVar9);
                                                          (*local_c0)(iVar9);
                                                          if (iVar2 < 0) {
                                                            uVar17 = 0x35be;
                                                          }
                                                          else {
                                                            if (iVar2 != 0) {
                                                              (*local_a4)(local_c4);
                                                              local_c4 = (int *)0x0;
                                                              (*local_a4)(local_c8);
                                                              local_c8 = (int *)0x0;
                                                              (*local_a4)(local_cc);
                                                              local_cc = (int *)0x0;
                                                              FUN_0001b800(*(undefined4 *)
                                                                            (local_70 + 0x50),
                                                                           local_d0,local_d4,
                                                                           local_d8);
                                                              goto LAB_0002da5c;
                                                            }
                                                            uVar17 = 0x35c6;
                                                            uVar16 = (*(code *)
                                                  PTR_PyThreadState_Get_0005240c)();
                                                  FUN_0001a5a0(uVar16,local_c4,local_c8,local_cc);
                                                  local_c4 = (int *)0x0;
                                                  local_c8 = (int *)0x0;
                                                  local_cc = (int *)0x0;
                                                  }
                                                  }
                                                  }
                                                  }
                                                  piVar3 = (int *)0x0;
                                                  FUN_0001b800(*(undefined4 *)(local_70 + 0x50),
                                                               local_d0,local_d4,local_d8);
                                                  uVar16 = 0x171;
                                                  piVar22 = (int *)0x0;
                                                  piVar21 = (int *)0x0;
                                                  piVar23 = local_c4;
                                                  goto LAB_0002bc58;
                                                  }
                                                  local_c4 = (int *)FUN_00018b60(piVar21,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2c40));
                                                  if (local_c4 == (int *)0x0) {
                                                    uVar16 = 0x3520;
                                                    goto LAB_0002d7a4;
                                                  }
                                                  local_4c = puVar11;
                                                  (*local_c0)(piVar21);
                                                  iVar5 = FUN_00018b90(local_b8,local_c4,2);
                                                  if (iVar5 < 0) {
                                                    uVar16 = 0x3523;
                                                    uVar17 = 0x172;
LAB_0002d948:
                                                    piVar21 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    goto LAB_0002d7a8;
                                                  }
                                                  (*local_c0)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  if (iVar5 != 0) {
                                                    if ((*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac
                                                                          ) + 0x10) ==
                                                         *(int *)(PTR_DAT_0005229c + 0x28b8)) &&
                                                       (*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac)
                                                                + 0x14) ==
                                                        *(int *)(PTR_DAT_0005229c + 0x28bc))) {
                                                      piVar21 = *(int **)(PTR_DAT_0005229c + 0x28b0)
                                                      ;
                                                      if (piVar21 == (int *)0x0) {
                                                        piVar21 = (int *)FUN_0001964c(*(undefined4 *
                                                                                       )(
                                                  PTR_DAT_0005229c + 0x2cb0));
                                                  goto LAB_0002d5fc;
                                                  }
                                                  *piVar21 = *piVar21 + 1;
LAB_0002cfe0:
                                                  local_cc = (int *)FUN_00018b60(piVar21,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2cfc));
                                                  if (local_cc == (int *)0x0) {
                                                    uVar16 = 0x3531;
                                                    piVar22 = (int *)0x0;
                                                  }
                                                  else {
                                                    (*local_c0)(piVar21);
                                                    piVar21 = (int *)(*(code *)
                                                  PTR_PyTuple_New_00052414)(4);
                                                  puVar11 = PTR_PyUnicode_Type_0005233c;
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar16 = 0x3534;
                                                  }
                                                  else {
                                                    piVar22 = *(int **)(PTR_DAT_0005229c + 0x2c3c);
                                                    *piVar22 = *piVar22 + 1;
                                                    piVar21[3] = (int)piVar22;
                                                    puVar24 = (undefined *)local_b8[1];
                                                    if (puVar24 == puVar11) {
                                                      *local_b8 = *local_b8 + 1;
                                                      piVar22 = local_b8;
                                                    }
                                                    else if ((puVar24 == PTR_PyLong_Type_00052384)
                                                            || (puVar24 == PTR_PyFloat_Type_00052520
                                                               )) {
                                                      piVar22 = (int *)(**(code **)(puVar24 + 0x44))
                                                                                 (local_b8);
                                                    }
                                                    else {
                                                      piVar22 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_b8,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar22 == (int *)0x0) {
                                                    uVar16 = 0x353c;
                                                    piVar22 = (int *)0x0;
                                                    local_c8 = (int *)0x0;
                                                  }
                                                  else {
                                                    uVar14 = 0x7f;
                                                    if ((piVar22[4] & 0x40U) == 0) {
                                                      uVar6 = piVar22[4] & 0x1c;
                                                      uVar14 = 0xff;
                                                      if ((uVar6 != 4) &&
                                                         (uVar14 = 0xffff, uVar6 != 8)) {
                                                        uVar14 = 0x10ffff;
                                                      }
                                                    }
                                                    local_48 = piVar22[2];
                                                    local_c8 = (int *)0x0;
                                                    piVar21[4] = (int)piVar22;
                                                    piVar22 = *(int **)(PTR_DAT_0005229c + 0x2c38);
                                                    *piVar22 = *piVar22 + 1;
                                                    piVar21[5] = (int)piVar22;
                                                    local_c8 = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2b84));
                                                  if (local_c8 == (int *)0x0) {
                                                    uVar16 = 0x3547;
                                                    piVar22 = (int *)0x0;
                                                  }
                                                  else {
                                                    piVar22 = (int *)FUN_00018b60(local_c8,*(
                                                  undefined4 *)(local_4c + 0x2c40));
                                                  if (piVar22 == (int *)0x0) {
                                                    uVar16 = 0x3549;
                                                  }
                                                  else {
                                                    (*local_c0)(local_c8);
                                                    puVar24 = (undefined *)piVar22[1];
                                                    local_c8 = (int *)0x0;
                                                    if (puVar24 == puVar11) {
                                                      *piVar22 = *piVar22 + 1;
                                                      local_c8 = piVar22;
                                                    }
                                                    else if ((puVar24 == PTR_PyLong_Type_00052384)
                                                            || (puVar24 == PTR_PyFloat_Type_00052520
                                                               )) {
                                                      local_c8 = (int *)(**(code **)(puVar24 + 0x44)
                                                                        )(piVar22);
                                                    }
                                                    else {
                                                      local_c8 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar22,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (local_c8 == (int *)0x0) {
                                                    uVar16 = 0x354c;
                                                    local_c8 = (int *)0x0;
                                                  }
                                                  else {
                                                    (*local_c0)(piVar22);
                                                    uVar6 = 0x7f;
                                                    if ((local_c8[4] & 0x40U) == 0) {
                                                      uVar8 = local_c8[4] & 0x1c;
                                                      uVar6 = 0xff;
                                                      if (uVar8 != 4) {
                                                        if (uVar8 == 8) {
                                                          uVar6 = 0xffff;
                                                        }
                                                        else {
                                                          uVar6 = 0x10ffff;
                                                        }
                                                      }
                                                    }
                                                    iVar5 = local_c8[2];
                                                    if (uVar6 <= uVar14) {
                                                      uVar6 = uVar14;
                                                    }
                                                    piVar21[6] = (int)local_c8;
                                                    local_c8 = (int *)0x0;
                                                    local_c8 = (int *)(*local_64)(piVar21,4,
                                                                                  iVar5 + 0x42 +
                                                                                  local_48,uVar6);
                                                    if (local_c8 == (int *)0x0) {
                                                      uVar16 = 0x3554;
                                                      piVar22 = (int *)0x0;
                                                      local_c8 = (int *)0x0;
                                                    }
                                                    else {
                                                      (*local_88)(piVar21);
                                                      if (((undefined *)local_cc[1] ==
                                                           PTR_PyMethod_Type_00052528) &&
                                                         (piVar21 = (int *)local_cc[3],
                                                         piVar21 != (int *)0x0)) {
                                                        local_cc = (int *)local_cc[2];
                                                        *piVar21 = *piVar21 + 1;
                                                        *local_cc = *local_cc + 1;
                                                        (*local_88)();
                                                        local_c4 = (int *)FUN_0001e58c(local_cc,
                                                  piVar21,local_c8);
                                                  }
                                                  else {
                                                    piVar21 = (int *)0x0;
                                                    local_c4 = (int *)FUN_0001e790(local_cc,local_c8
                                                                                  );
                                                  }
                                                  FUN_0001a404(piVar21);
                                                  (*local_88)(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  if (local_c4 != (int *)0x0) {
                                                    (*local_88)(local_cc);
                                                    local_cc = (int *)0x0;
                                                    (*local_88)(local_c4);
                                                    local_c4 = (int *)0x0;
                                                    local_c4 = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2b84));
                                                  if (local_c4 == (int *)0x0) {
                                                    uVar16 = 0x3570;
                                                  }
                                                  else {
                                                    local_cc = (int *)FUN_00018b60(local_c4,*(
                                                  undefined4 *)(local_4c + 0x2c40));
                                                  if (local_cc == (int *)0x0) {
                                                    uVar16 = 0x3572;
                                                  }
                                                  else {
                                                    (*local_88)(local_c4);
                                                    local_c4 = (int *)0x0;
                                                    local_c4 = (int *)FUN_0001ce3c(local_cc,local_b8
                                                                                  );
                                                    if (local_c4 != (int *)0x0) {
                                                      (*local_88)(local_cc);
                                                      local_cc = (int *)0x0;
                                                      iVar5 = FUN_0001ebb8(local_c4,piVar1);
                                                      pcVar20 = local_88;
                                                      if (iVar5 != -1) goto LAB_0002d328;
                                                      uVar16 = 0x3578;
                                                      uVar17 = 0x174;
                                                      goto LAB_0002d948;
                                                    }
                                                    uVar16 = 0x3575;
                                                  }
                                                  }
                                                  piVar22 = (int *)0x0;
                                                  piVar21 = (int *)0x0;
                                                  uVar17 = 0x174;
                                                  goto LAB_0002d7a8;
                                                  }
                                                  piVar21 = (int *)0x0;
                                                  uVar16 = 0x3564;
                                                  piVar22 = (int *)0x0;
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  else {
                                                    piVar21 = (int *)FUN_000196cc(*(undefined4 *)
                                                                                   (PTR_DAT_0005229c
                                                                                   + 0x2cb0),
                                                                                  PTR_DAT_0005229c +
                                                                                  0x28b8,
                                                  PTR_DAT_0005229c + 0x28b0);
LAB_0002d5fc:
                                                  if (piVar21 != (int *)0x0) goto LAB_0002cfe0;
                                                  piVar21 = (int *)0x0;
                                                  uVar16 = 0x352f;
                                                  piVar22 = (int *)0x0;
                                                  }
                                                  uVar17 = 0x173;
                                                  goto LAB_0002d7a8;
                                                  }
                                                  local_c4 = (int *)(*(code *)
                                                  PTR_PyList_New_00052548)(1);
                                                  if (local_c4 == (int *)0x0) {
                                                    uVar16 = 0x358d;
LAB_0002d9e0:
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x176;
                                                    goto LAB_0002d7a8;
                                                  }
                                                  *piVar1 = *piVar1 + 1;
                                                  *(int **)local_c4[3] = piVar1;
                                                  local_cc = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(local_7c + 0x2b84));
                                                  if (local_cc == (int *)0x0) {
                                                    uVar16 = 0x3592;
                                                    goto LAB_0002d9e0;
                                                  }
                                                  local_c8 = (int *)FUN_00018b60(local_cc,*(
                                                  undefined4 *)(puVar11 + 0x2c40));
                                                  if (local_c8 == (int *)0x0) {
                                                    uVar16 = 0x3594;
                                                    goto LAB_0002d9e0;
                                                  }
                                                  (*local_c0)(local_cc);
                                                  local_cc = (int *)0x0;
                                                  iVar5 = (*(code *)PTR_PyObject_SetItem_0005254c)
                                                                    (local_c8,local_b8,local_c4);
                                                  if (iVar5 < 0) {
                                                    uVar16 = 0x3597;
                                                    uVar17 = 0x176;
                                                    goto LAB_0002d948;
                                                  }
                                                  (*local_c0)(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  pcVar20 = local_c0;
LAB_0002d328:
                                                  (*pcVar20)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  (*local_a4)(local_d0);
                                                  local_d0 = 0;
                                                  (*local_a4)(local_d4);
                                                  local_d4 = 0;
                                                  (*local_a4)(local_d8);
                                                  local_d8 = 0;
                                                  local_d8 = FUN_000189e4(iVar2,*(undefined4 *)
                                                                                 (PTR_DAT_0005229c +
                                                                                 0x2a54),0);
                                                  (*local_c0)(iVar2);
                                                  if (local_d8 == 0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x35e0;
                                                    uVar16 = 0x171;
                                                    piVar21 = (int *)0x0;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(local_d8);
                                                  local_d8 = 0;
LAB_0002da5c:
                                                  piVar21 = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2e58));
                                                  local_c8 = piVar21;
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x35f6;
                                                    uVar16 = 0x177;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  local_c4 = (int *)0x0;
                                                  if (((undefined *)piVar21[1] ==
                                                       PTR_PyMethod_Type_00052528) &&
                                                     (local_c4 = (int *)piVar21[3],
                                                     local_c4 != (int *)0x0)) {
                                                    local_c8 = (int *)piVar21[2];
                                                    *local_c4 = *local_c4 + 1;
                                                    *local_c8 = *local_c8 + 1;
                                                    (*local_c0)(piVar21);
                                                    local_80 = 1;
                                                  }
                                                  if ((undefined *)local_c8[1] ==
                                                      PTR_PyFunction_Type_000523a4) {
                                                    local_ec = local_b0;
                                                    local_e8 = local_ac;
                                                    local_e0 = local_bc;
                                                    local_dc = local_78;
                                                    local_e4 = piVar15;
                                                    local_cc = (int *)FUN_0001d2c0(local_c8,&
                                                  local_ec + -local_80);
                                                  if (local_cc == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3607;
                                                    uVar16 = 0x177;
                                                    piVar21 = (int *)0x0;
                                                    piVar3 = (int *)0x0;
                                                    local_cc = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
LAB_0002dc40:
                                                  (*local_a4)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  }
                                                  else {
                                                    if (((undefined *)local_c8[1] ==
                                                         PTR_PyCFunction_Type_00052300) &&
                                                       ((*(uint *)(local_c8[2] + 8) & 0xffffff8d) ==
                                                        0x80)) {
                                                      local_ec = local_b0;
                                                      local_e8 = local_ac;
                                                      local_e0 = local_bc;
                                                      local_dc = local_78;
                                                      local_e4 = piVar15;
                                                      local_cc = (int *)FUN_0001838c(local_c8,&
                                                  local_ec + -local_80);
                                                  if (local_cc != (int *)0x0) goto LAB_0002dc40;
                                                  piVar3 = (int *)0x0;
                                                  piVar22 = (int *)0x0;
                                                  uVar17 = 0x360f;
                                                  uVar16 = 0x177;
                                                  piVar21 = (int *)0x0;
                                                  local_cc = (int *)0x0;
                                                  piVar23 = local_c4;
                                                  goto LAB_0002bc58;
                                                  }
                                                  piVar3 = (int *)(*(code *)PTR_PyTuple_New_00052414
                                                                  )(local_80 + 5);
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x3615;
                                                    uVar16 = 0x177;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  if (local_c4 != (int *)0x0) {
                                                    piVar3[3] = (int)local_c4;
                                                    local_c4 = (int *)0x0;
                                                  }
                                                  *(int *)local_b0 = *(int *)local_b0 + 1;
                                                  piVar3[local_80 + 3] = (int)local_b0;
                                                  *local_ac = *local_ac + 1;
                                                  piVar3[local_80 + 4] = (int)local_ac;
                                                  *piVar15 = *piVar15 + 1;
                                                  piVar3[local_80 + 5] = (int)piVar15;
                                                  *local_bc = *local_bc + 1;
                                                  piVar3[local_80 + 6] = (int)local_bc;
                                                  *local_78 = *local_78 + 1;
                                                  piVar3[local_80 + 7] = (int)local_78;
                                                  local_cc = (int *)FUN_000189e4(local_c8,piVar3,0);
                                                  if (local_cc == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3629;
                                                    uVar16 = 0x177;
                                                    piVar21 = (int *)0x0;
                                                    local_cc = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(piVar3);
                                                  }
                                                  (*local_c0)(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  (*local_c0)(local_cc);
                                                  local_cc = (int *)0x0;
                                                  local_c8 = (int *)FUN_00018b60(piVar1,*(undefined4
                                                                                          *)(
                                                  PTR_DAT_0005229c + 0x2adc));
                                                  if (local_c8 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3637;
                                                    uVar16 = 0x178;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  if (((undefined *)local_c8[1] ==
                                                       PTR_PyMethod_Type_00052528) &&
                                                     (piVar21 = (int *)local_c8[3],
                                                     piVar21 != (int *)0x0)) {
                                                    piVar3 = (int *)local_c8[2];
                                                    *piVar21 = *piVar21 + 1;
                                                    *piVar3 = *piVar3 + 1;
                                                    piVar22 = local_c8;
                                                    local_c8 = piVar3;
                                                    (*local_c0)(piVar22);
                                                    local_cc = (int *)FUN_0001e790(local_c8,piVar21)
                                                    ;
                                                  }
                                                  else {
                                                    piVar21 = (int *)0x0;
                                                    local_cc = (int *)FUN_0001e6dc(local_c8);
                                                  }
                                                  (*local_a4)(piVar21);
                                                  piVar3 = (int *)0x0;
                                                  if (local_cc == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3645;
                                                    uVar16 = 0x178;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(local_c8);
                                                  iVar2 = local_94[2];
                                                  local_c8 = (int *)0x0;
                                                  local_94[2] = (int)local_cc;
                                                  (*local_c0)(iVar2);
                                                  local_cc = (int *)0x0;
                                                  if ((undefined *)local_94[2] ==
                                                      PTR__Py_NoneStruct_000523c8) {
                                                    local_cc = (int *)FUN_0001c304(local_a8);
                                                    if (local_cc == (int *)0x0) {
                                                      piVar3 = (int *)0x0;
                                                      piVar22 = (int *)0x0;
                                                      uVar17 = 0x365b;
                                                      uVar16 = 0x179;
                                                      piVar21 = (int *)0x0;
                                                      piVar23 = local_c4;
                                                      goto LAB_0002bc58;
                                                    }
                                                    iVar2 = FUN_00018b90(piVar10,local_cc,3);
                                                    if (iVar2 < 0) {
                                                      uVar17 = 0x365d;
                                                      uVar16 = 0x179;
                                                      piVar3 = (int *)0x0;
                                                      piVar22 = (int *)0x0;
                                                      piVar21 = (int *)0x0;
                                                      piVar23 = local_c4;
                                                      goto LAB_0002bc58;
                                                    }
                                                    (*local_c0)(local_cc);
                                                    local_cc = (int *)0x0;
                                                    if (iVar2 == 0) goto LAB_0002ebe4;
                                                  }
                                                  local_cc = (int *)0x0;
                                                  if ((*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac)
                                                               + 0x10) ==
                                                       *(int *)(PTR_DAT_0005229c + 0x28a8)) &&
                                                     (*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac) +
                                                              0x14) ==
                                                      *(int *)(PTR_DAT_0005229c + 0x28ac))) {
                                                    piVar21 = *(int **)(PTR_DAT_0005229c + 0x28a0);
                                                    if (piVar21 == (int *)0x0) {
                                                      piVar21 = (int *)FUN_0001964c(*(undefined4 *)
                                                                                     (
                                                  PTR_DAT_0005229c + 0x2cb0));
                                                  }
                                                  else {
                                                    *piVar21 = *piVar21 + 1;
                                                  }
                                                  }
                                                  else {
                                                    piVar21 = (int *)FUN_000196cc(*(undefined4 *)
                                                                                   (PTR_DAT_0005229c
                                                                                   + 0x2cb0),
                                                                                  PTR_DAT_0005229c +
                                                                                  0x28a8,
                                                  PTR_DAT_0005229c + 0x28a0);
                                                  }
                                                  local_c8 = piVar21;
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x366b;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  piVar3 = (int *)FUN_00018b60(piVar21,*(undefined4
                                                                                         *)(
                                                  PTR_DAT_0005229c + 0x2cfc));
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x366d;
                                                    uVar16 = 0x17a;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  local_c8 = (int *)(*(code *)
                                                  PTR_PyTuple_New_00052414)(0xc);
                                                  puVar11 = PTR_PyUnicode_Type_0005233c;
                                                  if (local_c8 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3670;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  piVar21 = *(int **)(PTR_DAT_0005229c + 0x2b60);
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[3] = (int)piVar21;
                                                  piVar21 = (int *)local_94[2];
                                                  puVar24 = (undefined *)piVar21[1];
                                                  if (puVar24 == puVar11) {
                                                    *piVar21 = *piVar21 + 1;
                                                  }
                                                  else if ((puVar24 == PTR_PyLong_Type_00052384) ||
                                                          (puVar24 == PTR_PyFloat_Type_00052520)) {
                                                    piVar21 = (int *)(**(code **)(puVar24 + 0x44))
                                                                               (piVar21);
                                                  }
                                                  else {
                                                    piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar21,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  puVar24 = PTR_DAT_0005229c;
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3678;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = (int *)0x0;
                                                    goto LAB_0002bc58;
                                                  }
                                                  uVar14 = 0x7f;
                                                  if ((piVar21[4] & 0x40U) == 0) {
                                                    uVar6 = piVar21[4] & 0x1c;
                                                    uVar14 = 0xff;
                                                    if ((uVar6 != 4) &&
                                                       (uVar14 = 0xffff, uVar6 != 8)) {
                                                      uVar14 = 0x10ffff;
                                                    }
                                                  }
                                                  local_98 = (code *)piVar21[2];
                                                  local_c4 = (int *)0x0;
                                                  local_c8[4] = (int)piVar21;
                                                  piVar21 = *(int **)(puVar24 + 0x2df8);
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[5] = (int)piVar21;
                                                  puVar24 = (undefined *)piVar10[1];
                                                  if (puVar24 == puVar11) {
                                                    *piVar10 = *piVar10 + 1;
                                                    piVar21 = piVar10;
                                                  }
                                                  else if ((puVar24 == PTR_PyLong_Type_00052384) ||
                                                          (puVar24 == PTR_PyFloat_Type_00052520)) {
                                                    piVar21 = (int *)(**(code **)(puVar24 + 0x44))
                                                                               (piVar10);
                                                  }
                                                  else {
                                                    piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar10,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  puVar24 = PTR_DAT_0005229c;
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3683;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = (int *)0x0;
                                                    goto LAB_0002bc58;
                                                  }
                                                  uVar6 = 0x7f;
                                                  if ((piVar21[4] & 0x40U) == 0) {
                                                    uVar8 = piVar21[4] & 0x1c;
                                                    uVar6 = 0xff;
                                                    if (uVar8 != 4) {
                                                      if (uVar8 == 8) {
                                                        uVar6 = 0xffff;
                                                      }
                                                      else {
                                                        uVar6 = 0x10ffff;
                                                      }
                                                    }
                                                  }
                                                  if (uVar14 < uVar6) {
                                                    uVar14 = uVar6;
                                                  }
                                                  local_80 = piVar21[2];
                                                  local_c4 = (int *)0x0;
                                                  local_c8[6] = (int)piVar21;
                                                  piVar21 = *(int **)(puVar24 + 0x2dbc);
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[7] = (int)piVar21;
                                                  puVar24 = *(undefined **)(local_b0 + 4);
                                                  if (puVar24 == puVar11) {
                                                    *(int *)local_b0 = *(int *)local_b0 + 1;
                                                    pcVar20 = local_b0;
                                                  }
                                                  else if ((puVar24 == PTR_PyLong_Type_00052384) ||
                                                          (puVar24 == PTR_PyFloat_Type_00052520)) {
                                                    pcVar20 = (code *)(**(code **)(puVar24 + 0x44))
                                                                                (local_b0);
                                                  }
                                                  else {
                                                    pcVar20 = (code *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_b0,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  puVar24 = PTR_DAT_0005229c;
                                                  if (pcVar20 == (code *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x368e;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = (int *)0x0;
                                                    goto LAB_0002bc58;
                                                  }
                                                  uVar6 = 0x7f;
                                                  if ((*(uint *)(pcVar20 + 0x10) & 0x40) == 0) {
                                                    uVar8 = *(uint *)(pcVar20 + 0x10) & 0x1c;
                                                    uVar6 = 0xff;
                                                    if ((uVar8 != 4) && (uVar6 = 0xffff, uVar8 != 8)
                                                       ) {
                                                      uVar6 = 0x10ffff;
                                                    }
                                                  }
                                                  if (uVar14 < uVar6) {
                                                    uVar14 = uVar6;
                                                  }
                                                  local_78 = *(int **)(pcVar20 + 8);
                                                  local_c4 = (int *)0x0;
                                                  local_c8[8] = (int)pcVar20;
                                                  piVar21 = *(int **)(puVar24 + 11000);
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[9] = (int)piVar21;
                                                  puVar24 = (undefined *)local_ac[1];
                                                  local_98 = local_98 + 0x7c;
                                                  if (puVar24 == puVar11) {
                                                    *local_ac = *local_ac + 1;
                                                    piVar21 = local_ac;
                                                  }
                                                  else if ((puVar24 == PTR_PyLong_Type_00052384) ||
                                                          (puVar24 == PTR_PyFloat_Type_00052520)) {
                                                    piVar21 = (int *)(**(code **)(puVar24 + 0x44))
                                                                               (local_ac);
                                                  }
                                                  else {
                                                    piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_ac,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3699;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = (int *)0x0;
                                                    goto LAB_0002bc58;
                                                  }
                                                  uVar6 = 0x7f;
                                                  if ((piVar21[4] & 0x40U) == 0) {
                                                    uVar8 = piVar21[4] & 0x1c;
                                                    uVar6 = 0xff;
                                                    if (uVar8 != 4) {
                                                      if (uVar8 == 8) {
                                                        uVar6 = 0xffff;
                                                      }
                                                      else {
                                                        uVar6 = 0x10ffff;
                                                      }
                                                    }
                                                  }
                                                  if (uVar6 <= uVar14) {
                                                    uVar6 = uVar14;
                                                  }
                                                  iVar2 = piVar21[2];
                                                  piVar22 = *(int **)(PTR_DAT_0005229c + 0x2ce8);
                                                  local_c8[10] = (int)piVar21;
                                                  local_c4 = (int *)0x0;
                                                  *piVar22 = *piVar22 + 1;
                                                  local_c8[0xb] = (int)piVar22;
                                                  local_98 = local_98 + local_80 + (int)local_78;
                                                  piVar23 = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2cf0));
                                                  if (piVar23 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x36a4;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    goto LAB_0002bc58;
                                                  }
                                                  puVar24 = (undefined *)piVar23[1];
                                                  local_c4 = piVar23;
                                                  if (puVar24 == puVar11) {
                                                    *piVar23 = *piVar23 + 1;
                                                  }
                                                  else {
                                                    if ((puVar24 == PTR_PyLong_Type_00052384) ||
                                                       (puVar24 == PTR_PyFloat_Type_00052520)) {
                                                      piVar23 = (int *)(**(code **)(puVar24 + 0x44))
                                                                                 (piVar23);
                                                    }
                                                    else {
                                                      piVar23 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar23,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar23 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x36a6;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  (*local_88)(local_c4);
                                                  pcVar20 = local_98;
                                                  local_c4 = (int *)0x0;
                                                  uVar14 = 0x7f;
                                                  if ((piVar23[4] & 0x40U) == 0) {
                                                    uVar8 = piVar23[4] & 0x1c;
                                                    uVar14 = 0xff;
                                                    if (uVar8 != 4) {
                                                      if (uVar8 == 8) {
                                                        uVar14 = 0xffff;
                                                      }
                                                      else {
                                                        uVar14 = 0x10ffff;
                                                      }
                                                    }
                                                  }
                                                  if (uVar6 < uVar14) {
                                                    uVar6 = uVar14;
                                                  }
                                                  iVar5 = piVar23[2];
                                                  piVar21 = *(int **)(PTR_DAT_0005229c + 0x2b50);
                                                  local_c8[0xc] = (int)piVar23;
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[0xd] = (int)piVar21;
                                                  piVar22 = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2b84));
                                                  if (piVar22 == (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x36b2;
                                                    uVar16 = 0x17a;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  local_c4 = (int *)FUN_00018b60(piVar22,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2c04));
                                                  if (local_c4 == (int *)0x0) {
                                                    uVar17 = 0x36b4;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_88)(piVar22);
                                                  puVar24 = (undefined *)local_c4[1];
                                                  if (puVar24 == puVar11) {
                                                    *local_c4 = *local_c4 + 1;
                                                    piVar21 = local_c4;
                                                  }
                                                  else if ((puVar24 == PTR_PyLong_Type_00052384) ||
                                                          (puVar24 == PTR_PyFloat_Type_00052520)) {
                                                    piVar21 = (int *)(**(code **)(puVar24 + 0x44))
                                                                               (local_c4);
                                                  }
                                                  else {
                                                    piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_c4,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x36b7;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  FUN_00019ba8(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  uVar14 = 0x7f;
                                                  if ((piVar21[4] & 0x40U) == 0) {
                                                    uVar8 = piVar21[4] & 0x1c;
                                                    uVar14 = 0xff;
                                                    if (uVar8 != 4) {
                                                      if (uVar8 == 8) {
                                                        uVar14 = 0xffff;
                                                      }
                                                      else {
                                                        uVar14 = 0x10ffff;
                                                      }
                                                    }
                                                  }
                                                  iVar9 = piVar21[2];
                                                  if (uVar14 <= uVar6) {
                                                    uVar14 = uVar6;
                                                  }
                                                  local_c8[0xe] = (int)piVar21;
                                                  iVar2 = FUN_00019cec(local_c8,0xc,
                                                                       pcVar20 + iVar9 + iVar5 + 
                                                  iVar2,uVar14);
                                                  if (iVar2 == 0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x36bf;
                                                    uVar16 = 0x17a;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  FUN_00019ba8(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  piVar23 = piVar3;
                                                  if (((undefined *)piVar3[1] ==
                                                       PTR_PyMethod_Type_00052528) &&
                                                     (local_c8 = (int *)piVar3[3],
                                                     local_c8 != (int *)0x0)) {
                                                    piVar23 = (int *)piVar3[2];
                                                    *local_c8 = *local_c8 + 1;
                                                    *piVar23 = *piVar23 + 1;
                                                    FUN_00019ba8(piVar3);
                                                  }
                                                  if (local_c8 == (int *)0x0) {
                                                    local_cc = (int *)FUN_0001e790(piVar23,iVar2);
                                                  }
                                                  else {
                                                    local_cc = (int *)FUN_0001e58c(piVar23,local_c8,
                                                                                   iVar2);
                                                  }
                                                  FUN_0001a404(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  FUN_00019ba8(iVar2);
                                                  if (local_cc != (int *)0x0) {
                                                    FUN_00019ba8(piVar23);
                                                    goto LAB_0002e328;
                                                  }
                                                  piVar22 = (int *)0x0;
                                                  uVar17 = 0x36cf;
                                                  uVar16 = 0x17a;
                                                  piVar21 = (int *)0x0;
                                                  piVar3 = piVar23;
                                                  piVar23 = local_c4;
                                                  goto LAB_0002bc58;
                                                  }
                                                  uVar17 = 0x3508;
                                                  }
                                                  uVar16 = 0x171;
                                                  (*local_c0)(iVar2);
                                                  piVar22 = (int *)0x0;
                                                  piVar21 = (int *)0x0;
                                                  piVar23 = local_c4;
                                                  goto LAB_0002bc58;
                                                  }
LAB_0002ebe4:
                                                  puVar11 = PTR_DAT_0005229c;
                                                  piVar3 = (int *)(*local_9c)(local_a0,*(undefined4
                                                                                         *)(
                                                  PTR_DAT_0005229c + 0x2c0c));
                                                  piVar13 = piVar1;
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x36f6;
                                                    uVar16 = 0x17c;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  piVar22 = (int *)(*local_9c)(piVar3,*(undefined4 *
                                                                                       )(
                                                  PTR_DAT_0005229c + 0x2c44));
                                                  if (piVar22 == (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x36f8;
                                                    uVar16 = 0x17c;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(piVar3);
                                                  local_c8 = (int *)(*local_9c)(local_a0,*(
                                                  undefined4 *)(puVar11 + 0x2c0c));
                                                  if (local_c8 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x36fb;
                                                    uVar16 = 0x17c;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  local_c4 = (int *)(*local_9c)(local_c8,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2c94));
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x36fd;
                                                    uVar16 = 0x17c;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  local_88 = (code *)PTR_PyMethod_Type_00052528;
                                                  if (((undefined *)local_c4[1] ==
                                                       PTR_PyMethod_Type_00052528) &&
                                                     (local_c8 = (int *)local_c4[3],
                                                     local_c8 != (int *)0x0)) {
                                                    local_c4 = (int *)local_c4[2];
                                                    *local_c8 = *local_c8 + 1;
                                                    *local_c4 = *local_c4 + 1;
                                                    (*local_c0)();
                                                    if (local_c8 == (int *)0x0) goto LAB_0002f4f8;
                                                    piVar3 = (int *)FUN_0001e790();
                                                  }
                                                  else {
LAB_0002f4f8:
                                                    piVar3 = (int *)FUN_0001e6dc(local_c4);
                                                  }
                                                  (*local_a4)(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x370c;
                                                    uVar16 = 0x17c;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  local_c4 = (int *)FUN_00028c48(piVar3,*(undefined4
                                                                                          *)(
                                                  PTR_DAT_0005229c + 0x2aa0),5);
                                                  if (local_c4 == (int *)0x0) {
                                                    uVar17 = 0x370f;
                                                    uVar16 = 0x17c;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = (int *)0x0;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(piVar3);
                                                  if (((undefined *)piVar22[1] ==
                                                       PTR_PyMethod_Type_00052528) &&
                                                     (piVar21 = (int *)piVar22[3],
                                                     piVar21 != (int *)0x0)) {
                                                    piVar3 = (int *)piVar22[2];
                                                    *piVar21 = *piVar21 + 1;
                                                    *piVar3 = *piVar3 + 1;
                                                    (*local_c0)(piVar22);
                                                    local_cc = (int *)FUN_0001e58c(piVar3,piVar21,
                                                                                   local_c4);
                                                    piVar22 = piVar3;
                                                  }
                                                  else {
                                                    local_cc = (int *)FUN_0001e790(piVar22,local_c4)
                                                    ;
                                                    piVar21 = (int *)0x0;
                                                  }
                                                  (*local_a4)(piVar21);
                                                  (*local_c0)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  if (local_cc == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x371f;
                                                    uVar16 = 0x17c;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  (*local_c0)(piVar22);
                                                  (*local_c0)(local_cc);
                                                  local_74 = local_74 + 1;
                                                  local_cc = (int *)0x0;
                                                  } while (local_74 != local_44);
                                                  if ((*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac)
                                                               + 0x10) ==
                                                       *(int *)(PTR_DAT_0005229c + 0x2898)) &&
                                                     (*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac) +
                                                              0x14) ==
                                                      *(int *)(PTR_DAT_0005229c + 0x289c))) {
                                                    piVar22 = *(int **)(PTR_DAT_0005229c + 0x2890);
                                                    if (piVar22 == (int *)0x0) {
                                                      piVar22 = (int *)FUN_0001964c(*(undefined4 *)
                                                                                     (
                                                  PTR_DAT_0005229c + 0x2cb0));
                                                  goto LAB_0002f53c;
                                                  }
                                                  *piVar22 = *piVar22 + 1;
                                                  }
                                                  else {
                                                    piVar22 = (int *)FUN_000196cc(*(undefined4 *)
                                                                                   (PTR_DAT_0005229c
                                                                                   + 0x2cb0),
                                                                                  PTR_DAT_0005229c +
                                                                                  0x2898,
                                                  PTR_DAT_0005229c + 0x2890);
LAB_0002f53c:
                                                  if (piVar22 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x372d;
                                                    uVar16 = 0x17f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  local_98 = (code *)(PTR_LAB_000522a8 + -0x74a0);
                                                  local_c4 = (int *)FUN_00018b60(piVar22,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2ad0));
                                                  if (local_c4 == (int *)0x0) {
                                                    uVar17 = 0x372f;
                                                    piVar21 = (int *)0x0;
                                                    uVar16 = 0x17f;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    (*local_c0)(piVar22);
                                                    piVar22 = (int *)(*(code *)
                                                  PTR_PyTuple_New_00052414)(10);
                                                  if (piVar22 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x3732;
                                                    uVar16 = 0x17f;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    piVar21 = *(int **)(PTR_DAT_0005229c + 0x2eb4);
                                                    *piVar21 = *piVar21 + 1;
                                                    piVar22[3] = (int)piVar21;
                                                    local_88 = (code *)PTR_PyUnicode_Type_0005233c;
                                                    puVar11 = (undefined *)piVar10[1];
                                                    if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                      *piVar10 = *piVar10 + 1;
                                                      piVar21 = piVar10;
                                                    }
                                                    else {
                                                      if ((puVar11 == PTR_PyLong_Type_00052384) ||
                                                         (puVar11 == PTR_PyFloat_Type_00052520)) {
                                                        piVar21 = (int *)(**(code **)(puVar11 + 0x44
                                                                                     ))(piVar10);
                                                      }
                                                      else {
                                                        piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar10,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x373a;
                                                    uVar16 = 0x17f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  local_88 = (code *)0x7f;
                                                  if ((piVar21[4] & 0x40U) == 0) {
                                                    uVar14 = piVar21[4] & 0x1c;
                                                    local_88 = (code *)0xff;
                                                    if (uVar14 != 4) {
                                                      if (uVar14 == 8) {
                                                        local_88 = (code *)0xffff;
                                                      }
                                                      else {
                                                        local_88 = (code *)0x10ffff;
                                                      }
                                                    }
                                                  }
                                                  local_80 = piVar21[2];
                                                  piVar22[4] = (int)piVar21;
                                                  piVar21 = *(int **)(PTR_DAT_0005229c + 0x2dbc);
                                                  *piVar21 = *piVar21 + 1;
                                                  piVar22[5] = (int)piVar21;
                                                  puVar11 = *(undefined **)(local_b0 + 4);
                                                  if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                    *(int *)local_b0 = *(int *)local_b0 + 1;
                                                    pcVar20 = local_b0;
                                                  }
                                                  else {
                                                    if ((puVar11 == PTR_PyLong_Type_00052384) ||
                                                       (puVar11 == PTR_PyFloat_Type_00052520)) {
                                                      pcVar20 = (code *)(**(code **)(puVar11 + 0x44)
                                                                        )(local_b0);
                                                    }
                                                    else {
                                                      pcVar20 = (code *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_b0,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (pcVar20 == (code *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x3745;
                                                    uVar16 = 0x17f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  pcVar18 = (code *)0x7f;
                                                  if ((*(uint *)(pcVar20 + 0x10) & 0x40) == 0) {
                                                    uVar14 = *(uint *)(pcVar20 + 0x10) & 0x1c;
                                                    pcVar18 = (code *)0xff;
                                                    if ((uVar14 != 4) &&
                                                       (pcVar18 = (code *)0xffff, uVar14 != 8)) {
                                                      pcVar18 = (code *)0x10ffff;
                                                    }
                                                  }
                                                  local_78 = *(int **)(pcVar20 + 8);
                                                  piVar22[6] = (int)pcVar20;
                                                  piVar21 = *(int **)(PTR_DAT_0005229c + 11000);
                                                  *piVar21 = *piVar21 + 1;
                                                  piVar22[7] = (int)piVar21;
                                                  puVar11 = (undefined *)local_ac[1];
                                                  if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                    *local_ac = *local_ac + 1;
                                                    piVar21 = local_ac;
                                                  }
                                                  else {
                                                    if ((puVar11 == PTR_PyLong_Type_00052384) ||
                                                       (puVar11 == PTR_PyFloat_Type_00052520)) {
                                                      piVar21 = (int *)(**(code **)(puVar11 + 0x44))
                                                                                 (local_ac);
                                                    }
                                                    else {
                                                      piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_ac,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x3750;
                                                    uVar16 = 0x17f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  pcVar20 = (code *)0x7f;
                                                  if ((piVar21[4] & 0x40U) == 0) {
                                                    uVar14 = piVar21[4] & 0x1c;
                                                    pcVar20 = (code *)0xff;
                                                    if ((uVar14 != 4) &&
                                                       (pcVar20 = (code *)0xffff, uVar14 != 8)) {
                                                      pcVar20 = (code *)0x10ffff;
                                                    }
                                                  }
                                                  local_74 = piVar21[2];
                                                  piVar22[8] = (int)piVar21;
                                                  piVar21 = *(int **)(PTR_DAT_0005229c + 0x2ce8);
                                                  *piVar21 = *piVar21 + 1;
                                                  piVar22[9] = (int)piVar21;
                                                  piVar3 = (int *)(*local_98)(local_a0,*(undefined4
                                                                                         *)(
                                                  PTR_DAT_0005229c + 0x2cf0));
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x375b;
                                                    uVar16 = 0x17f;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    puVar11 = (undefined *)piVar3[1];
                                                    if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                      *piVar3 = *piVar3 + 1;
                                                      local_c8 = piVar3;
                                                    }
                                                    else if ((puVar11 == PTR_PyLong_Type_00052384)
                                                            || (puVar11 == PTR_PyFloat_Type_00052520
                                                               )) {
                                                      local_c8 = (int *)(**(code **)(puVar11 + 0x44)
                                                                        )(piVar3);
                                                    }
                                                    else {
                                                      local_c8 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar3,*(undefined4 *)
                                                                     (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (local_c8 == (int *)0x0) {
                                                    uVar17 = 0x375d;
                                                    uVar16 = 0x17f;
                                                    piVar21 = (int *)0x0;
                                                    local_c8 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    pcVar12 = (code *)0x7f;
                                                    (*local_c0)(piVar3);
                                                    if ((local_c8[4] & 0x40U) == 0) {
                                                      uVar14 = local_c8[4] & 0x1c;
                                                      pcVar12 = (code *)0xff;
                                                      if ((uVar14 != 4) &&
                                                         (pcVar12 = (code *)0xffff, uVar14 != 8)) {
                                                        pcVar12 = (code *)0x10ffff;
                                                      }
                                                    }
                                                    local_70 = local_c8[2];
                                                    piVar22[10] = (int)local_c8;
                                                    local_c8 = (int *)0x0;
                                                    piVar21 = *(int **)(PTR_DAT_0005229c + 0x2b50);
                                                    *piVar21 = *piVar21 + 1;
                                                    piVar22[0xb] = (int)piVar21;
                                                    local_c8 = (int *)(*local_98)(local_a0,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2b84));
                                                  if (local_c8 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x3769;
                                                    uVar16 = 0x17f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    piVar3 = (int *)(*local_98)(local_c8,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2c04));
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x376b;
                                                    uVar16 = 0x17f;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    (*local_c0)(local_c8);
                                                    puVar11 = (undefined *)piVar3[1];
                                                    local_c8 = (int *)0x0;
                                                    if (puVar11 == PTR_PyUnicode_Type_0005233c) {
                                                      *piVar3 = *piVar3 + 1;
                                                      local_c8 = piVar3;
                                                    }
                                                    else if ((puVar11 == PTR_PyLong_Type_00052384)
                                                            || (puVar11 == PTR_PyFloat_Type_00052520
                                                               )) {
                                                      local_c8 = (int *)(**(code **)(puVar11 + 0x44)
                                                                        )(piVar3);
                                                    }
                                                    else {
                                                      local_c8 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar3,*(undefined4 *)
                                                                     (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (local_c8 == (int *)0x0) {
                                                    uVar17 = 0x376e;
                                                    uVar16 = 0x17f;
                                                    piVar21 = (int *)0x0;
                                                    local_c8 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    (*local_c0)(piVar3);
                                                    pcVar4 = (code *)0x7f;
                                                    if ((local_c8[4] & 0x40U) == 0) {
                                                      uVar14 = local_c8[4] & 0x1c;
                                                      pcVar4 = (code *)0xff;
                                                      if (uVar14 != 4) {
                                                        if (uVar14 == 8) {
                                                          pcVar4 = (code *)0xffff;
                                                        }
                                                        else {
                                                          pcVar4 = (code *)0x10ffff;
                                                        }
                                                      }
                                                    }
                                                    iVar2 = local_c8[2];
                                                    if (pcVar18 <= local_88) {
                                                      pcVar18 = local_88;
                                                    }
                                                    if (pcVar20 <= pcVar18) {
                                                      pcVar20 = pcVar18;
                                                    }
                                                    if (pcVar12 <= pcVar20) {
                                                      pcVar12 = pcVar20;
                                                    }
                                                    if (pcVar4 <= pcVar12) {
                                                      pcVar4 = pcVar12;
                                                    }
                                                    piVar22[0xc] = (int)local_c8;
                                                    local_c8 = (int *)0x0;
                                                    local_c8 = (int *)FUN_00019cec(piVar22,10,
                                                                                   (int)local_78 +
                                                                                   local_74 +
                                                                                   local_70 + iVar2
                                                                                   + 0x52 + local_80
                                                                                   ,pcVar4);
                                                    if (local_c8 == (int *)0x0) {
                                                      piVar3 = (int *)0x0;
                                                      uVar17 = 0x3776;
                                                      uVar16 = 0x17f;
                                                      piVar21 = (int *)0x0;
                                                      local_c8 = (int *)0x0;
                                                      piVar23 = local_c4;
                                                    }
                                                    else {
                                                      (*local_c0)(piVar22);
                                                      if (((undefined *)local_c4[1] ==
                                                           PTR_PyMethod_Type_00052528) &&
                                                         (piVar21 = (int *)local_c4[3],
                                                         piVar21 != (int *)0x0)) {
                                                        local_c4 = (int *)local_c4[2];
                                                        *piVar21 = *piVar21 + 1;
                                                        *local_c4 = *local_c4 + 1;
                                                        (*local_c0)();
                                                        local_cc = (int *)FUN_0001e58c(local_c4,
                                                  piVar21,local_c8);
                                                  }
                                                  else {
                                                    piVar21 = (int *)0x0;
                                                    local_cc = (int *)FUN_0001e790(local_c4,local_c8
                                                                                  );
                                                  }
                                                  local_88 = (code *)(PTR_LAB_000522a8 + -0x5bfc);
                                                  FUN_0001a404(piVar21);
                                                  FUN_00019ba8(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  if (local_cc == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3786;
                                                    uVar16 = 0x17f;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    FUN_00019ba8(local_c4);
                                                    local_c4 = (int *)0x0;
                                                    FUN_00019ba8(local_cc);
                                                    puVar11 = PTR_DAT_0005229c;
                                                    local_cc = (int *)0x0;
                                                    local_c4 = (int *)(*local_98)(local_a0,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2c0c));
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3792;
                                                    uVar16 = 0x180;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    local_c8 = (int *)(*local_98)(local_c4,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2c44));
                                                  if (local_c8 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3794;
                                                    uVar16 = 0x180;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    FUN_00019ba8(local_c4);
                                                    local_c4 = (int *)0x0;
                                                    piVar22 = (int *)(*local_98)(local_a0,*(
                                                  undefined4 *)(puVar11 + 0x2c0c));
                                                  if (piVar22 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x3797;
                                                    uVar16 = 0x180;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    piVar3 = (int *)(*local_98)(piVar22,*(undefined4
                                                                                          *)(
                                                  PTR_DAT_0005229c + 0x2c94));
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    uVar17 = 0x3799;
                                                    uVar16 = 0x180;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    FUN_00019ba8(piVar22);
                                                    puVar11 = PTR_PyMethod_Type_00052528;
                                                    if (((undefined *)piVar3[1] ==
                                                         PTR_PyMethod_Type_00052528) &&
                                                       (piVar21 = (int *)piVar3[3],
                                                       piVar21 != (int *)0x0)) {
                                                      piVar22 = (int *)piVar3[2];
                                                      *piVar21 = *piVar21 + 1;
                                                      *piVar22 = *piVar22 + 1;
                                                      FUN_00019ba8(piVar3);
                                                      local_c4 = (int *)FUN_0001e790(piVar22,piVar21
                                                                                    );
                                                      piVar3 = piVar22;
                                                    }
                                                    else {
                                                      local_c4 = (int *)FUN_0001e6dc(piVar3);
                                                      piVar21 = (int *)0x0;
                                                    }
                                                    (*local_88)(piVar21);
                                                    if (local_c4 == (int *)0x0) {
                                                      piVar22 = (int *)0x0;
                                                      uVar17 = 0x37a8;
                                                      uVar16 = 0x180;
                                                      piVar21 = (int *)0x0;
                                                      piVar23 = local_c4;
                                                    }
                                                    else {
                                                      FUN_00019ba8(piVar3);
                                                      iVar2 = FUN_00028c48(local_c4,*(undefined4 *)
                                                                                     (
                                                  PTR_DAT_0005229c + 0x2a94),10);
                                                  if (iVar2 == 0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x37ab;
                                                    uVar16 = 0x180;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    FUN_00019ba8(local_c4);
                                                    local_c4 = (int *)0x0;
                                                    if (((undefined *)local_c8[1] == puVar11) &&
                                                       (local_c4 = (int *)local_c8[3],
                                                       local_c4 != (int *)0x0)) {
                                                      local_c8 = (int *)local_c8[2];
                                                      *local_c4 = *local_c4 + 1;
                                                      *local_c8 = *local_c8 + 1;
                                                      FUN_00019ba8();
                                                      if (local_c4 == (int *)0x0) goto LAB_0002f744;
                                                      local_cc = (int *)FUN_0001e58c(local_c8,
                                                  local_c4,iVar2);
                                                  }
                                                  else {
LAB_0002f744:
                                                    local_cc = (int *)FUN_0001e790(local_c8,iVar2);
                                                  }
                                                  (*local_88)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  FUN_00019ba8(iVar2);
                                                  if (local_cc == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x37bb;
                                                    uVar16 = 0x180;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    FUN_00019ba8(local_c8);
                                                    local_c8 = (int *)0x0;
LAB_0002e328:
                                                    FUN_00019ba8(local_cc);
                                                    local_cc = (int *)0x0;
                                                    piVar13 = piVar1;
                                                    if ((int *)local_94[2] == local_68) {
                                                      if ((*(int *)(*(int *)(PTR_DAT_0005229c +
                                                                            0x2fac) + 0x10) ==
                                                           *(int *)(PTR_DAT_0005229c + 0x2888)) &&
                                                         (*(int *)(*(int *)(PTR_DAT_0005229c +
                                                                           0x2fac) + 0x14) ==
                                                          *(int *)(PTR_DAT_0005229c + 0x288c))) {
                                                        piVar21 = *(int **)(PTR_DAT_0005229c +
                                                                           0x2880);
                                                        if (piVar21 == (int *)0x0) {
                                                          piVar21 = (int *)FUN_0001964c(*(undefined4
                                                                                          *)(
                                                  PTR_DAT_0005229c + 0x2cb0));
                                                  }
                                                  else {
                                                    *piVar21 = *piVar21 + 1;
                                                  }
                                                  }
                                                  else {
                                                    piVar21 = (int *)FUN_000196cc(*(undefined4 *)
                                                                                   (PTR_DAT_0005229c
                                                                                   + 0x2cb0),
                                                                                  PTR_DAT_0005229c +
                                                                                  0x2888,
                                                  PTR_DAT_0005229c + 0x2880);
                                                  }
                                                  local_c8 = piVar21;
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x37d4;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    piVar3 = (int *)(*local_9c)(piVar21,*(undefined4
                                                                                          *)(
                                                  PTR_DAT_0005229c + 0x2ad0));
                                                  if (piVar3 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x37d6;
                                                    uVar16 = 0x183;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    (*local_c0)(local_c8);
                                                    local_c8 = (int *)0x0;
                                                    local_c8 = (int *)(*(code *)
                                                  PTR_PyTuple_New_00052414)(10);
                                                  puVar11 = PTR_PyUnicode_Type_0005233c;
                                                  if (local_c8 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x37d9;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    piVar21 = *(int **)(PTR_DAT_0005229c + 0x2df0);
                                                    *piVar21 = *piVar21 + 1;
                                                    local_c8[3] = (int)piVar21;
                                                    puVar24 = (undefined *)piVar10[1];
                                                    if (puVar24 == puVar11) {
                                                      *piVar10 = *piVar10 + 1;
                                                      piVar21 = piVar10;
                                                    }
                                                    else if ((puVar24 == PTR_PyLong_Type_00052384)
                                                            || (puVar24 == PTR_PyFloat_Type_00052520
                                                               )) {
                                                      piVar21 = (int *)(**(code **)(puVar24 + 0x44))
                                                                                 (piVar10);
                                                    }
                                                    else {
                                                      piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar10,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x37e1;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = (int *)0x0;
                                                  }
                                                  else {
                                                    uVar14 = 0x7f;
                                                    if ((piVar21[4] & 0x40U) == 0) {
                                                      uVar6 = piVar21[4] & 0x1c;
                                                      uVar14 = 0xff;
                                                      if ((uVar6 != 4) &&
                                                         (uVar14 = 0xffff, uVar6 != 8)) {
                                                        uVar14 = 0x10ffff;
                                                      }
                                                    }
                                                    iVar2 = piVar21[2];
                                                    piVar22 = *(int **)(local_3c + 0x2dbc);
                                                    local_c8[4] = (int)piVar21;
                                                    local_c4 = (int *)0x0;
                                                    *piVar22 = *piVar22 + 1;
                                                    local_c8[5] = (int)piVar22;
                                                    puVar24 = *(undefined **)(local_b0 + 4);
                                                    if (puVar24 == puVar11) {
                                                      *(int *)local_b0 = *(int *)local_b0 + 1;
                                                      pcVar20 = local_b0;
                                                    }
                                                    else if ((puVar24 == PTR_PyLong_Type_00052384)
                                                            || (puVar24 == PTR_PyFloat_Type_00052520
                                                               )) {
                                                      pcVar20 = (code *)(**(code **)(puVar24 + 0x44)
                                                                        )(local_b0);
                                                    }
                                                    else {
                                                      pcVar20 = (code *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_b0,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  puVar24 = PTR_DAT_0005229c;
                                                  if (pcVar20 == (code *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x37ec;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = (int *)0x0;
                                                  }
                                                  else {
                                                    uVar6 = 0x7f;
                                                    if ((*(uint *)(pcVar20 + 0x10) & 0x40) == 0) {
                                                      uVar8 = *(uint *)(pcVar20 + 0x10) & 0x1c;
                                                      uVar6 = 0xff;
                                                      if (uVar8 != 4) {
                                                        if (uVar8 == 8) {
                                                          uVar6 = 0xffff;
                                                        }
                                                        else {
                                                          uVar6 = 0x10ffff;
                                                        }
                                                      }
                                                    }
                                                    if (uVar14 < uVar6) {
                                                      uVar14 = uVar6;
                                                    }
                                                    local_b0 = *(code **)(pcVar20 + 8);
                                                    local_c4 = (int *)0x0;
                                                    local_c8[6] = (int)pcVar20;
                                                    piVar21 = *(int **)(puVar24 + 0x2af4);
                                                    *piVar21 = *piVar21 + 1;
                                                    local_c8[7] = (int)piVar21;
                                                    puVar24 = (undefined *)local_ac[1];
                                                    if (puVar24 == puVar11) {
                                                      *local_ac = *local_ac + 1;
                                                      piVar21 = local_ac;
                                                    }
                                                    else if ((puVar24 == PTR_PyLong_Type_00052384)
                                                            || (puVar24 == PTR_PyFloat_Type_00052520
                                                               )) {
                                                      piVar21 = (int *)(**(code **)(puVar24 + 0x44))
                                                                                 (local_ac);
                                                    }
                                                    else {
                                                      piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_ac,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x37f7;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = (int *)0x0;
                                                  }
                                                  else {
                                                    uVar6 = 0x7f;
                                                    if ((piVar21[4] & 0x40U) == 0) {
                                                      uVar8 = piVar21[4] & 0x1c;
                                                      uVar6 = 0xff;
                                                      if ((uVar8 != 4) &&
                                                         (uVar6 = 0xffff, uVar8 != 8)) {
                                                        uVar6 = 0x10ffff;
                                                      }
                                                    }
                                                    if (uVar14 < uVar6) {
                                                      uVar14 = uVar6;
                                                    }
                                                    local_ac = (int *)piVar21[2];
                                                    local_c4 = (int *)0x0;
                                                    local_c8[8] = (int)piVar21;
                                                    piVar21 = *(int **)(local_38 + 0x2ce8);
                                                    *piVar21 = *piVar21 + 1;
                                                    local_c8[9] = (int)piVar21;
                                                    pcVar20 = local_b0 + iVar2 + 100;
                                                    local_b0 = (code *)(PTR_LAB_000522a8 + -0x74a0);
                                                    piVar23 = (int *)FUN_00018b60(local_a0,*(
                                                  undefined4 *)(local_54 + 0x2cf0));
                                                  if (piVar23 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3802;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                  }
                                                  else {
                                                    puVar24 = (undefined *)piVar23[1];
                                                    local_c4 = piVar23;
                                                    if (puVar24 == puVar11) {
                                                      *piVar23 = *piVar23 + 1;
                                                    }
                                                    else {
                                                      if ((puVar24 == PTR_PyLong_Type_00052384) ||
                                                         (puVar24 == PTR_PyFloat_Type_00052520)) {
                                                        piVar23 = (int *)(**(code **)(puVar24 + 0x44
                                                                                     ))(piVar23);
                                                      }
                                                      else {
                                                        piVar23 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (piVar23,*(undefined4 *)
                                                                      (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar23 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3804;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                    goto LAB_0002bc58;
                                                  }
                                                  }
                                                  (*local_c0)(local_c4);
                                                  local_c4 = (int *)0x0;
                                                  uVar6 = 0x7f;
                                                  if ((piVar23[4] & 0x40U) == 0) {
                                                    uVar8 = piVar23[4] & 0x1c;
                                                    uVar6 = 0xff;
                                                    if (uVar8 != 4) {
                                                      if (uVar8 == 8) {
                                                        uVar6 = 0xffff;
                                                      }
                                                      else {
                                                        uVar6 = 0x10ffff;
                                                      }
                                                    }
                                                  }
                                                  if (uVar6 <= uVar14) {
                                                    uVar6 = uVar14;
                                                  }
                                                  iVar2 = piVar23[2];
                                                  piVar21 = *(int **)(local_34 + 0x2b50);
                                                  local_c8[10] = (int)piVar23;
                                                  *piVar21 = *piVar21 + 1;
                                                  local_c8[0xb] = (int)piVar21;
                                                  pcVar20 = pcVar20 + (int)local_ac;
                                                  piVar22 = (int *)(*local_b0)(local_a0,*(undefined4
                                                                                          *)(
                                                  local_7c + 0x2b84));
                                                  if (piVar22 == (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    uVar17 = 0x3810;
                                                    uVar16 = 0x183;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    local_c4 = (int *)(*local_b0)(piVar22,*(
                                                  undefined4 *)(local_50 + 0x2c04));
                                                  if (local_c4 == (int *)0x0) {
                                                    uVar17 = 0x3812;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    (*local_c0)(piVar22);
                                                    puVar24 = (undefined *)local_c4[1];
                                                    if (puVar24 == puVar11) {
                                                      *local_c4 = *local_c4 + 1;
                                                      piVar21 = local_c4;
                                                    }
                                                    else if ((puVar24 == PTR_PyLong_Type_00052384)
                                                            || (puVar24 == PTR_PyFloat_Type_00052520
                                                               )) {
                                                      piVar21 = (int *)(**(code **)(puVar24 + 0x44))
                                                                                 (local_c4);
                                                    }
                                                    else {
                                                      piVar21 = (int *)(*(code *)
                                                  PTR_PyObject_Format_00052518)
                                                            (local_c4,*(undefined4 *)
                                                                       (PTR_DAT_0005229c + 0x2f98));
                                                  }
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3815;
                                                    uVar16 = 0x183;
                                                    piVar21 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    (*local_c0)(local_c4);
                                                    local_c4 = (int *)0x0;
                                                    uVar14 = 0x7f;
                                                    if ((piVar21[4] & 0x40U) == 0) {
                                                      uVar8 = piVar21[4] & 0x1c;
                                                      uVar14 = 0xff;
                                                      if (uVar8 != 4) {
                                                        if (uVar8 == 8) {
                                                          uVar14 = 0xffff;
                                                        }
                                                        else {
                                                          uVar14 = 0x10ffff;
                                                        }
                                                      }
                                                    }
                                                    iVar5 = piVar21[2];
                                                    if (uVar14 <= uVar6) {
                                                      uVar14 = uVar6;
                                                    }
                                                    local_c8[0xc] = (int)piVar21;
                                                    iVar2 = (*local_64)(local_c8,10,
                                                                        pcVar20 + iVar5 + iVar2,
                                                                        uVar14);
                                                    if (iVar2 == 0) {
                                                      piVar22 = (int *)0x0;
                                                      uVar17 = 0x381d;
                                                      uVar16 = 0x183;
                                                      piVar21 = (int *)0x0;
                                                      piVar23 = local_c4;
                                                    }
                                                    else {
                                                      (*local_c0)(local_c8);
                                                      local_c8 = (int *)0x0;
                                                      piVar23 = piVar3;
                                                      if (((undefined *)piVar3[1] ==
                                                           PTR_PyMethod_Type_00052528) &&
                                                         (local_c8 = (int *)piVar3[3],
                                                         local_c8 != (int *)0x0)) {
                                                        piVar23 = (int *)piVar3[2];
                                                        *local_c8 = *local_c8 + 1;
                                                        *piVar23 = *piVar23 + 1;
                                                        (*local_c0)(piVar3);
                                                      }
                                                      if (local_c8 == (int *)0x0) {
                                                        local_cc = (int *)FUN_0001e790(piVar23,iVar2
                                                                                      );
                                                      }
                                                      else {
                                                        local_cc = (int *)FUN_0001e58c(piVar23,
                                                  local_c8,iVar2);
                                                  }
                                                  (*local_a4)(local_c8);
                                                  local_c8 = (int *)0x0;
                                                  (*local_c0)(iVar2);
                                                  piVar22 = (int *)0x0;
                                                  if (local_cc != (int *)0x0) {
                                                    piVar21 = (int *)0x0;
                                                    (*local_c0)(piVar23);
                                                    (*local_c0)(local_cc);
                                                    local_cc = (int *)0x0;
                                                    piVar23 = (int *)local_94[2];
                                                    *piVar23 = *piVar23 + 1;
                                                    goto LAB_0002e82c;
                                                  }
                                                  uVar17 = 0x382d;
                                                  uVar16 = 0x183;
                                                  piVar21 = (int *)0x0;
                                                  piVar3 = piVar23;
                                                  piVar23 = local_c4;
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  else {
                                                    puVar7 = (undefined *)
                                                             FUN_00019888(*(undefined4 *)
                                                                           (PTR_DAT_0005229c +
                                                                           0x2f6c),*(undefined4 *)
                                                                                    (
                                                  PTR_DAT_0005229c + 0x2fa0),0);
                                                  puVar24 = PTR__Py_NoneStruct_000523c8;
                                                  puVar11 = PTR_LAB_000522b0;
                                                  if (puVar7 == (undefined *)0x0) {
                                                    uVar16 = 0x3296;
                                                    *local_68 = *local_68 + 1;
                                                    puVar7 = puVar24;
                                                  }
                                                  else {
                                                    *(int **)(puVar7 + 8) = local_94;
                                                    *local_94 = *local_94 + 1;
                                                    piVar21 = (int *)FUN_00028e14(*(undefined4 *)
                                                                                   (PTR_DAT_0005229c
                                                                                   + 0x2f80),
                                                                                  puVar11 + -0x57c4,
                                                                                  puVar7,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2d4c),
                                                  *(undefined4 *)(PTR_DAT_0005229c + 0x2ed4),
                                                  *(undefined4 *)(PTR_DAT_0005229c + 0x2d78));
                                                  if (piVar21 != (int *)0x0) {
                                                    (*local_c0)(puVar7);
                                                    local_cc = piVar21;
                                                    piVar21 = (int *)(*(code *)
                                                  PTR_PyUnicode_Join_000524f8)
                                                            (*(undefined4 *)
                                                              (PTR_DAT_0005229c + 0x2e60),piVar21);
                                                  if (piVar21 == (int *)0x0) {
                                                    piVar22 = (int *)0x0;
                                                    uVar17 = 0x3850;
                                                    uVar16 = 0x185;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    (*local_c0)(local_cc);
                                                    local_cc = (int *)0x0;
                                                    if ((*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac
                                                                          ) + 0x10) ==
                                                         *(int *)(PTR_DAT_0005229c + 0x2878)) &&
                                                       (*(int *)(*(int *)(PTR_DAT_0005229c + 0x2fac)
                                                                + 0x14) ==
                                                        *(int *)(PTR_DAT_0005229c + 0x287c))) {
                                                      piVar22 = *(int **)(PTR_DAT_0005229c + 0x2870)
                                                      ;
                                                      if (piVar22 == (int *)0x0) {
                                                        piVar22 = (int *)FUN_0001964c(*(undefined4 *
                                                                                       )(
                                                  PTR_DAT_0005229c + 0x2cb0));
                                                  }
                                                  else {
                                                    *piVar22 = *piVar22 + 1;
                                                  }
                                                  }
                                                  else {
                                                    piVar22 = (int *)FUN_000196cc(*(undefined4 *)
                                                                                   (PTR_DAT_0005229c
                                                                                   + 0x2cb0),
                                                                                  PTR_DAT_0005229c +
                                                                                  0x2878,
                                                  PTR_DAT_0005229c + 0x2870);
                                                  }
                                                  local_cc = piVar22;
                                                  if (piVar22 == (int *)0x0) {
                                                    uVar17 = 0x385d;
                                                    uVar16 = 0x186;
                                                    piVar22 = (int *)0x0;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    piVar22 = (int *)(*local_9c)(piVar22,*(
                                                  undefined4 *)(local_40 + 0x2cfc));
                                                  if (piVar22 == (int *)0x0) {
                                                    uVar17 = 0x385f;
                                                    uVar16 = 0x186;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    iVar2 = 0;
                                                    (*local_c0)(local_cc);
                                                    local_cc = (int *)0x0;
                                                    if (((undefined *)piVar22[1] ==
                                                         PTR_PyMethod_Type_00052528) &&
                                                       (local_cc = (int *)piVar22[3],
                                                       local_cc != (int *)0x0)) {
                                                      piVar3 = (int *)piVar22[2];
                                                      *local_cc = *local_cc + 1;
                                                      *piVar3 = *piVar3 + 1;
                                                      (*local_c0)(piVar22);
                                                      iVar2 = 1;
                                                      piVar22 = piVar3;
                                                    }
                                                    if ((undefined *)piVar22[1] ==
                                                        PTR_PyFunction_Type_000523a4) {
                                                      local_ec = *(code **)(PTR_DAT_0005229c +
                                                                           0x2dec);
                                                      local_e8 = piVar21;
                                                      iVar2 = FUN_0001d2c0(piVar22,&local_ec +
                                                                                   -iVar2);
                                                      if (iVar2 == 0) {
                                                        uVar17 = 0x3871;
                                                        uVar16 = 0x186;
                                                        piVar3 = (int *)0x0;
                                                        piVar23 = local_c4;
                                                      }
                                                      else {
LAB_0002fc64:
                                                        (*local_a4)(local_cc);
                                                        local_cc = (int *)0x0;
LAB_0002fc74:
                                                        (*local_c0)(piVar22);
                                                        (*local_c0)(iVar2);
                                                        iVar2 = local_94[2];
                                                        if (*(undefined **)(iVar2 + 4) ==
                                                            PTR_PyDict_Type_00052394) {
                                                          piVar23 = (int *)FUN_0001b190(iVar2,*(
                                                  undefined4 *)(PTR_DAT_0005229c + 0x2c8c));
                                                  }
                                                  else {
                                                    piVar23 = (int *)(*(code *)
                                                  PTR_PyObject_GetItem_00052498)
                                                            (iVar2,*(undefined4 *)
                                                                    (PTR_DAT_0005229c + 0x2c8c));
                                                  }
                                                  if (piVar23 != (int *)0x0) goto LAB_0002e82c;
                                                  uVar17 = 0x3899;
                                                  uVar16 = 0x187;
                                                  piVar22 = (int *)0x0;
                                                  piVar3 = (int *)0x0;
                                                  piVar23 = local_c4;
                                                  }
                                                  }
                                                  else if (((undefined *)piVar22[1] ==
                                                            PTR_PyCFunction_Type_00052300) &&
                                                          ((*(uint *)(piVar22[2] + 8) & 0xffffff8d)
                                                           == 0x80)) {
                                                    local_ec = *(code **)(PTR_DAT_0005229c + 0x2dec)
                                                    ;
                                                    local_e8 = piVar21;
                                                    iVar2 = FUN_0001838c(piVar22,&local_ec + -iVar2)
                                                    ;
                                                    if (iVar2 != 0) goto LAB_0002fc64;
                                                    uVar17 = 0x3879;
                                                    uVar16 = 0x186;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    local_c8 = (int *)(*(code *)
                                                  PTR_PyTuple_New_00052414)(iVar2 + 2);
                                                  if (local_c8 == (int *)0x0) {
                                                    uVar17 = 0x387f;
                                                    uVar16 = 0x186;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    if (local_cc != (int *)0x0) {
                                                      local_c8[3] = (int)local_cc;
                                                      local_cc = (int *)0x0;
                                                    }
                                                    piVar3 = *(int **)(PTR_DAT_0005229c + 0x2dec);
                                                    *piVar3 = *piVar3 + 1;
                                                    local_c8[iVar2 + 3] = (int)piVar3;
                                                    *piVar21 = *piVar21 + 1;
                                                    local_c8[iVar2 + 4] = (int)piVar21;
                                                    iVar2 = FUN_000189e4(piVar22,local_c8,0);
                                                    if (iVar2 != 0) {
                                                      (*local_c0)(local_c8);
                                                      local_c8 = (int *)0x0;
                                                      goto LAB_0002fc74;
                                                    }
                                                    uVar17 = 0x388a;
                                                    uVar16 = 0x186;
                                                    piVar3 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  goto LAB_0002bc58;
                                                  }
                                                  uVar16 = 0x329e;
                                                  }
                                                  FUN_0001ac3c(PTR_DAT_000522ac + -0x1f3c,uVar16,
                                                               0x185,PTR_DAT_000522ac + -0x2380);
                                                  uVar17 = 0x384e;
                                                  (*local_c0)(puVar7);
                                                  uVar16 = 0x185;
                                                  local_cc = (int *)0x0;
                                                  piVar22 = (int *)0x0;
                                                  piVar21 = (int *)0x0;
                                                  piVar3 = (int *)0x0;
                                                  piVar23 = local_c4;
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  else {
                                                    local_c4 = (int *)FUN_0001cbec(piVar10,*(
                                                  undefined4 *)(puVar11 + 0x2a7c));
                                                  if (local_c4 == (int *)0x0) {
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    local_bc = (int *)0x0;
                                                    uVar17 = 0x33b6;
                                                    uVar16 = 0x162;
                                                    piVar15 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  else {
                                                    iVar2 = FUN_00018be8(local_c4);
                                                    if (-1 < iVar2) {
                                                      (*local_84)(local_c4);
                                                      if (iVar2 == 0) goto LAB_0002c4f4;
                                                      piVar15 = *(int **)(PTR_DAT_0005229c + 0x2f5c)
                                                      ;
                                                      *piVar15 = *piVar15 + 1;
                                                      goto LAB_0002c44c;
                                                    }
                                                    uVar17 = 0x33b8;
                                                    uVar16 = 0x162;
                                                    piVar3 = (int *)0x0;
                                                    piVar22 = (int *)0x0;
                                                    piVar21 = (int *)0x0;
                                                    piVar13 = (int *)0x0;
                                                    local_b8 = (int *)0x0;
                                                    local_bc = (int *)0x0;
                                                    piVar15 = (int *)0x0;
                                                    piVar23 = local_c4;
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
LAB_0002bc58:
  local_c4 = piVar23;
  (*local_90)(local_c4);
  (*local_90)(local_c8);
  (*local_90)(local_cc);
  piVar23 = (int *)0x0;
  (*local_90)(piVar22);
  (*local_90)(piVar3);
  FUN_0001ac3c(PTR_DAT_000522ac + -0x1f88,uVar17,uVar16,PTR_DAT_000522ac + -0x2380);
  piVar1 = piVar13;
LAB_0002e82c:
  (*local_90)(local_8c);
  (*local_90)(local_a8);
  (*local_90)(local_b4);
  (*local_90)(piVar10);
  (*local_90)(piVar15);
  (*local_90)(local_bc);
  (*local_90)(local_b8);
  (*local_90)(piVar1);
  (*local_90)(piVar21);
  (*local_84)(local_94);
  return piVar23;
}


