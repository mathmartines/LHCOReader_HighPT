"""Helper class to construct the efficiency matrix."""

import numpy as np


class EfficiencyFileBuilder:
    """Constructs the file for the Efficiency matrix"""
    # information needed for the files
    banner_info = "Experiment Search ll~ qq~ FF XY coef type Nevs"

    def __init__(self):
        # All banner info are initialized with None value
        self.__dict__ = {info: None for info in self.banner_info.split()}
        self.kernel = np.array([])
        self.xsections = np.array([])
        self.bin_edges = np.array([])

    @property
    def llbar(self):
        """returns the flavor of the leptons"""
        return self.__getattribute__("ll~")

    @llbar.setter
    def llbar(self, final_leptons):
        self.__setattr__("ll~", final_leptons)

    @property
    def qqbar(self):
        """Returns the initial quarks flavors"""
        return self.__getattribute__("qq~")

    @qqbar.setter
    def qqbar(self, initial_quarks):
        self.__setattr__("qq~", initial_quarks)

    def build_file(self):
        """Constrocts the file using the current information available on 'banner_info' variable"""
        return self.construct_header() + self.construct_content()

    def construct_header(self):
        """Constructs the information about the file"""
        banner_info = "#===============\n"
        banner_info += "\n".join(
            [f"# {info} : {self.__getattribute__(info)}" for info in self.banner_info.split()]) + "\n"
        banner_info += "#===============\n"
        banner_info += "#\n"
        banner_info += "# XSEC	BIN_MIN	BIN_MAX 	 Kij\n"
        banner_info += "# " + " ".join([f"{bin_edge:.0f}" for bin_edge in self.bin_edges]) + "\n"
        return banner_info

    def construct_content(self):
        """Builds the efficiency matrices for the file"""
        low_bin_values, high_bin_values = self.bin_edges[:-1], self.bin_edges[1:]
        additional_info = np.array([self.xsections, low_bin_values, high_bin_values])
        # information with the same columns as in High-Pt
        all_info = np.concatenate((additional_info.transpose(), self.kernel), axis=1)
        # Transforms to string
        return "\n".join([" ".join([f"{val:.4e}" for val in line]) for line in all_info])
