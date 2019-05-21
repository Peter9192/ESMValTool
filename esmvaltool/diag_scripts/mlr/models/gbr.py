"""Gradient Boosting Regression model."""

import logging
import os

import matplotlib.pyplot as plt
import numpy as np

from esmvaltool.diag_scripts.mlr.models import MLRModel

logger = logging.getLogger(os.path.basename(__file__))


class GBRModel(MLRModel):
    """Base class for Gradient Boosting Regression models.

    Note
    ----
    See :mod:`esmvaltool.diag_scripts.mlr.models`.

    """

    _CLF_TYPE = None

    def plot_gbr_feature_importance(self, filename=None):
        """Plot GBR feature importance.

        Note
        ----
        In contrast to the general implementation of feature importance using
        model scoring or prediction variance (done via the module
        :mod:`skater`), this function uses a specific procedure for GBR based
        on the number of appearances of that feature in the regression trees
        and the improvements made by the individual splits (see Friedman,
        2001).

        Parameters
        ----------
        filename : str, optional (default: 'feature_importance_gbr')
           Name of the plot file.

        """
        if not self._is_ready_for_plotting():
            return
        logger.info("Plotting GBR feature importance")
        if filename is None:
            filename = 'gbr_feature_importance'
        (_, axes) = plt.subplots()
        clf = self._clf.steps[-1][1].regressor_

        # Plot
        feature_importance = clf.feature_importances_
        sorted_idx = np.argsort(feature_importance)
        pos = np.arange(sorted_idx.shape[0]) + 0.5
        axes.barh(pos, feature_importance[sorted_idx], align='center')
        axes.set_title(f'Variable Importance ({str(self._CLF_TYPE)} Model)')
        axes.set_xlabel('Relative Importance')
        axes.set_yticks(pos)
        axes.set_yticklabels(self.features[sorted_idx])
        new_filename = filename + '.' + self._cfg['output_file_type']
        new_path = os.path.join(self._cfg['mlr_plot_dir'], new_filename)
        plt.savefig(new_path, orientation='landscape', bbox_inches='tight')
        logger.info("Wrote %s", new_path)
        plt.close()

    def _plot_prediction_error(self,
                               train_score,
                               test_score=None,
                               filename=None):
        """Plot prediction error during fitting."""
        if not self._is_ready_for_plotting():
            return
        logger.info("Plotting prediction error")
        if filename is None:
            filename = 'prediction_error'
        (_, axes) = plt.subplots()
        x_values = np.arange(len(train_score), dtype=np.float64) + 1.0

        # Plot train score
        axes.plot(x_values, train_score, 'b-', label='Training Set Deviance')

        # Plot test score if possible
        if test_score is not None:
            axes.plot(x_values, test_score, 'r-', label='Test Set Deviance')

        # Appearance
        axes.legend(loc='upper right')
        axes.set_title(f'Deviance ({str(self._CLF_TYPE)} Model)')
        axes.set_xlabel('Boosting Iterations')
        axes.set_ylabel('Deviance')
        new_filename = filename + '.' + self._cfg['output_file_type']
        new_path = os.path.join(self._cfg['mlr_plot_dir'], new_filename)
        plt.savefig(new_path, orientation='landscape', bbox_inches='tight')
        logger.info("Wrote %s", new_path)
        plt.close()
