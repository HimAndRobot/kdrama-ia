import logging
import statistics


class CfsPrtouchBridge:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object("gcode")
        self.last_probe = None
        self.last_clear_path = None
        self.gcode.register_command(
            "CFS_PROBE_POINT",
            self.cmd_CFS_PROBE_POINT,
            desc=self.cmd_CFS_PROBE_POINT_help,
        )
        self.gcode.register_command(
            "CFS_TEST_CLEAR_PATH",
            self.cmd_CFS_TEST_CLEAR_PATH,
            desc=self.cmd_CFS_TEST_CLEAR_PATH_help,
        )

    cmd_CFS_PROBE_POINT_help = "probe a specific XY point through the native probe object and return the measured Z"
    cmd_CFS_TEST_CLEAR_PATH_help = "probe start/end points and wipe between them using measured Z values"

    def _find_prtouch(self):
        printer_objects = [name for name, _obj in self.printer.lookup_objects()]
        for name in ("prtouch_v3", "prtouch_v2", "prtouch"):
            if name in printer_objects:
                return self.printer.lookup_object(name)
        return None

    def _ensure_homed(self, prtouch):
        toolhead = self.printer.lookup_object("toolhead")
        status = toolhead.get_status(self.printer.get_reactor().monotonic())
        homed_axes = status.get("homed_axes", "")
        if set("xyz").issubset(set(homed_axes)):
            return
        self.gcode.run_script_from_command("G28")

    def _move_xyz(self, x=None, y=None, z=None, speed=150.0):
        parts = ["G1", "F%d" % int(float(speed) * 60.0)]
        if x is not None:
            parts.append("X%.3f" % float(x))
        if y is not None:
            parts.append("Y%.3f" % float(y))
        if z is not None:
            parts.append("Z%.3f" % float(z))
        self.gcode.run_script_from_command(" ".join(parts))

    def _set_hotend(self, temp, wait=False):
        code = "M109" if wait else "M104"
        self.gcode.run_script_from_command("%s S%d" % (code, int(round(float(temp)))))

    def _set_bed(self, temp, wait=False):
        code = "M190" if wait else "M140"
        self.gcode.run_script_from_command("%s S%d" % (code, int(round(float(temp)))))

    def _set_part_fan(self, speed):
        self.gcode.run_script_from_command("M106 S%d" % int(speed))

    def _run_probe_once(
        self,
        x,
        y,
        safe_z=10.0,
        probe_speed=2.0,
        sample_retract_dist=2.0,
    ):
        probe = self.printer.lookup_object("probe")
        self.gcode.run_script_from_command("G90")
        self._move_xyz(z=safe_z, speed=10.0)
        self._move_xyz(x=x, y=y, speed=150.0)
        self._move_xyz(z=safe_z, speed=10.0)
        probe_gcmd = self.gcode.create_gcode_command(
            "PROBE",
            "PROBE",
            {
                "PROBE_SPEED": str(float(probe_speed)),
                "SAMPLES": "1",
                "SAMPLE_RETRACT_DIST": str(float(sample_retract_dist)),
            },
        )
        pos = probe.run_probe(probe_gcmd)
        measured_z = float(pos[2])
        self.gcode.run_script_from_command("G90")
        self._move_xyz(z=safe_z, speed=10.0)
        return measured_z

    def probe_point(
        self,
        x,
        y,
        probe_speed=2.0,
        probe_times=3,
        sample_retract_dist=2.0,
        max_z_err=0.2,
        safe_z=10.0,
    ):
        values = []
        for _index in range(int(probe_times)):
            values.append(
                self._run_probe_once(
                    x=x,
                    y=y,
                    safe_z=safe_z,
                    probe_speed=probe_speed,
                    sample_retract_dist=sample_retract_dist,
                )
            )
        measured_z = float(statistics.median(values))
        spread = float(max(values) - min(values)) if values else 0.0
        self.last_probe = {
            "x": float(x),
            "y": float(y),
            "z": measured_z,
            "values": values,
            "spread": spread,
            "probe_speed": float(probe_speed),
            "probe_times": int(probe_times),
            "sample_retract_dist": float(sample_retract_dist),
            "max_z_err": float(max_z_err),
            "safe_z": float(safe_z),
        }
        if spread > float(max_z_err):
            raise self.printer.command_error(
                "Probe spread too large: %.4f > %.4f" % (spread, float(max_z_err))
            )
        logging.info(
            "[CFS_PROBE_POINT] x=%.3f y=%.3f z=%.3f spread=%.4f",
            float(x),
            float(y),
            measured_z,
            spread,
        )
        return measured_z

    def test_clear_path(
        self,
        start_x,
        start_y,
        end_x,
        end_y,
        safe_z=10.0,
        offset_z=-0.15,
        probe_speed=2.0,
        probe_times=3,
        sample_retract_dist=2.0,
        max_z_err=0.2,
        hot_min_temp=140.0,
        hot_max_temp=200.0,
        bed_temp=60.0,
        wipe_speed=2.0,
        travel_speed=150.0,
        passes=2,
    ):
        self._ensure_homed(self._find_prtouch())
        self._set_bed(bed_temp, wait=False)
        self._set_hotend(hot_min_temp, wait=False)
        self._set_hotend(hot_min_temp, wait=True)

        start_z = self.probe_point(
            x=start_x,
            y=start_y,
            probe_speed=probe_speed,
            probe_times=probe_times,
            sample_retract_dist=sample_retract_dist,
            max_z_err=max_z_err,
            safe_z=safe_z,
        )
        self._set_hotend(min(hot_min_temp + 40.0, hot_max_temp), wait=False)
        end_z = self.probe_point(
            x=end_x,
            y=end_y,
            probe_speed=probe_speed,
            probe_times=probe_times,
            sample_retract_dist=sample_retract_dist,
            max_z_err=max_z_err,
            safe_z=safe_z,
        )

        path_safe_z = max(float(safe_z), max(start_z, end_z) + 3.0)
        self.gcode.run_script_from_command("G90")
        self._move_xyz(z=path_safe_z, speed=10.0)
        self._move_xyz(x=start_x, y=start_y, speed=travel_speed)
        self._move_xyz(z=start_z + 0.2, speed=2.5)
        self._set_hotend(hot_max_temp, wait=True)
        self._set_hotend(hot_min_temp, wait=False)
        for _index in range(int(passes)):
            self._move_xyz(
                x=end_x,
                y=end_y,
                z=end_z + float(offset_z),
                speed=wipe_speed,
            )
            self._move_xyz(
                x=start_x,
                y=start_y,
                z=start_z + float(offset_z),
                speed=wipe_speed,
            )
        self._set_part_fan(255)
        self._set_hotend(hot_min_temp, wait=True)
        self._move_xyz(x=end_x + 10.0, y=end_y, z=end_z + 10.0, speed=wipe_speed)
        self._set_part_fan(0)
        self._set_bed(bed_temp, wait=True)
        self.last_clear_path = {
            "start_x": float(start_x),
            "start_y": float(start_y),
            "start_z": float(start_z),
            "end_x": float(end_x),
            "end_y": float(end_y),
            "end_z": float(end_z),
            "safe_z": float(path_safe_z),
            "offset_z": float(offset_z),
            "probe_times": int(probe_times),
            "max_z_err": float(max_z_err),
            "hot_min_temp": float(hot_min_temp),
            "hot_max_temp": float(hot_max_temp),
            "bed_temp": float(bed_temp),
            "wipe_speed": float(wipe_speed),
            "travel_speed": float(travel_speed),
            "passes": int(passes),
        }
        logging.info(
            "[CFS_TEST_CLEAR_PATH] start=(%.3f,%.3f,%.3f) end=(%.3f,%.3f,%.3f) offset=%.3f",
            float(start_x),
            float(start_y),
            float(start_z),
            float(end_x),
            float(end_y),
            float(end_z),
            float(offset_z),
        )
        return self.last_clear_path

    def get_status(self, eventtime):
        return {
            "last_probe": self.last_probe,
            "last_clear_path": self.last_clear_path,
        }

    def cmd_CFS_PROBE_POINT(self, gcmd):
        x = gcmd.get_float("X")
        y = gcmd.get_float("Y")
        measured_z = self.probe_point(
            x=x,
            y=y,
            probe_speed=gcmd.get_float("PROBE_SPEED", default=2.0, above=0.0),
            probe_times=gcmd.get_int("PROBE_TIMES", default=3, minval=1),
            sample_retract_dist=gcmd.get_float("SAMPLE_RETRACT_DIST", default=2.0, above=0.0),
            max_z_err=gcmd.get_float("MAX_Z_ERR", default=0.2, above=0.0),
            safe_z=gcmd.get_float("SAFE_Z", default=10.0),
        )
        gcmd.respond_info(
            "[CFS_PROBE_POINT] X=%.3f Y=%.3f Z=%.3f" % (float(x), float(y), measured_z)
        )

    def cmd_CFS_TEST_CLEAR_PATH(self, gcmd):
        result = self.test_clear_path(
            start_x=gcmd.get_float("START_X"),
            start_y=gcmd.get_float("START_Y"),
            end_x=gcmd.get_float("END_X"),
            end_y=gcmd.get_float("END_Y"),
            safe_z=gcmd.get_float("SAFE_Z", default=10.0),
            offset_z=gcmd.get_float("OFFSET_Z", default=-0.15),
            probe_speed=gcmd.get_float("PROBE_SPEED", default=2.0, above=0.0),
            probe_times=gcmd.get_int("PROBE_TIMES", default=3, minval=1),
            sample_retract_dist=gcmd.get_float("SAMPLE_RETRACT_DIST", default=2.0, above=0.0),
            max_z_err=gcmd.get_float("MAX_Z_ERR", default=0.2, above=0.0),
            hot_min_temp=gcmd.get_float("HOT_MIN_TEMP", default=140.0, above=0.0),
            hot_max_temp=gcmd.get_float("HOT_MAX_TEMP", default=200.0, above=0.0),
            bed_temp=gcmd.get_float("BED_TEMP", default=60.0, minval=0.0),
            wipe_speed=gcmd.get_float("WIPE_SPEED", default=2.0, above=0.0),
            travel_speed=gcmd.get_float("TRAVEL_SPEED", default=150.0, above=0.0),
            passes=gcmd.get_int("PASSES", default=2, minval=1),
        )
        gcmd.respond_info(
            "[CFS_TEST_CLEAR_PATH] start_z=%.3f end_z=%.3f"
            % (result["start_z"], result["end_z"])
        )


def load_config(config):
    return CfsPrtouchBridge(config)
