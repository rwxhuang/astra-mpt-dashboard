% Read data
tech_projs_df = readtable('./data/tech_projects_out.csv');
format long g
CovMatrix_Value1_norm = readmatrix('./data/cov_matrix.txt')
bounds = readmatrix('./data/bounds.txt')
% Create portfolios
p1=Portfolio('AssetList', tech_projs_df.Name);
p1=Portfolio(p1,'assetmean',tech_projs_df.value1_norm_mean,'AssetCovar',CovMatrix_Value1_norm);
p1=Portfolio(p1,'LowerBudget',1,'UpperBudget',1,'lowerbound',0);
nPortfolios=20;
lowerbounds = zeros(1, height(tech_projs_df)) + bounds(1, 1);
upperbounds= zeros(1, height(tech_projs_df)) + bounds(1, 2);
display(lowerbounds)
display(upperbounds)

p1_bound_minAssets = setMinMaxNumAssets(p1, 2, []);
p1_bound=setBounds(p1_bound_minAssets,lowerbounds, upperbounds, 'BoundType','Conditional');
pwgt1 = estimateFrontier(p1_bound,nPortfolios) ;
for i=1:size(pwgt1,2)
    PortfolioReturns1(i)=tech_projs_df.value1_norm_mean'*pwgt1(:,i);
end
% Figure 3
% f1 = figure('visible', 'off')
% subplot(2,1,1)
% plotFrontier(p1)
% title('Efficient Frontier Portfolio - Value1')
% hold on
% swgt1 = estimateMaxSharpeRatio(p1);
% [srsk1,sret1] = estimatePortMoments(p1,swgt1);
% plot(srsk1,sret1,'r*','MarkerSize',8)
% plot(sqrt(tech_projs_df.value1_norm_var),tech_projs_df.value1_norm_mean,'ko','MarkerSize',6,'LineWidth',1)
% text(sqrt(tech_projs_df.value1_norm_var)*1.025,tech_projs_df.value1_norm_mean*1.015,tech_projs_df.Name,'FontSize',12)
% subplot(2,1,2)
% pie(pwgt1(:,4)) %plotting 5th portfolio
% legend(tech_projs_df.Name)
% title('allocation of 4th portfolio-Value1')
% set(gca,'FontSize',14)
% grid on
% ylabel('Project(Asset)Fraction for Investment')
% saveas(gcf,'./out/mpt_graph_3.png')
% Figure 4
% f4 = figure('visible', 'off')
% plotFrontier(p1)
% hold on
[rsk1,ret1] = estimatePortMoments(p1,pwgt1);
writematrix([rsk1, ret1], './out/risk_return.txt')
% plot(rsk1,ret1,'.','MarkerSize',20)
% plot(sqrt(tech_projs_df.value1_norm_var),tech_projs_df.value1_norm_mean,'ko','MarkerSize',6,'LineWidth',1)
% text(sqrt(tech_projs_df.value1_norm_var)*1.025,tech_projs_df.value1_norm_mean*1.015,tech_projs_df.Name,'FontSize',12)
% title('Efficient Frontier')
% saveas(gcf,'./out/mpt_graph_4.png')
% Figure 5
% f5 = figure('visible', 'off')
% bar(pwgt1')
% legend(tech_projs_df.Name)
% set(gca,'FontSize',14)
% grid on
% ylabel('Project(Asset)Fraction for Investment')
% saveas(gcf,'./out/mpt_graph_5.png')
% Figure 6
% f6 = figure('visible', 'off')
% plotFrontier(p1)
% title('Efficient Frontier Portfolio - Value computed from f_1')
% hold on

% [rsk1,ret1] = estimatePortMoments(p1,pwgt1);
% plot(rsk1,ret1,'o','MarkerSize',8,'MarkerFaceColor',[0.5 0.5 0.5],'MarkerEdgeColor',[0.5 0.5 0.5])

% plot(rsk1(7),ret1(7),'o','MarkerSize',8,'MarkerFaceColor','r','MarkerEdgeColor','r')

%get portfolio with maximum sharpe ratio (return to risk)
% swgt1 = estimateMaxSharpeRatio(p1);
% [srsk1,sret1] = estimatePortMoments(p1,swgt1);

%plot(srsk1,sret1,'r^','MarkerSize',7,'MarkerFaceColor','r')
% set(gca,'FontSize',14)

%plot assets' risk and mean return
% plot(sqrt(tech_projs_df.value1_norm_var),tech_projs_df.value1_norm_mean,'ks','MarkerSize',6,'MarkerFaceColor','k','LineWidth',1)
% text(sqrt(tech_projs_df.value1_norm_var)*1.025,tech_projs_df.value1_norm_mean*1.015,tech_projs_df.Name,'FontSize',12)
% legend({'efficient frontier','efficient portfolios','example portfolio','Instruments'})

% xstart=.50;
% xend=.8;
% ystart=0.03;
% yend=0.8;
% axes('position',[xstart ystart xend-xstart yend-ystart ])
% box on

%pie(swgt1) %plotting sharpe portfolio
% pie(pwgt1(:,7)) %plotting 7th portfolio
% set(gca,'FontSize',12)
% legend(tech_projs_df.Name)
% title('example portfolio')
% set(gca,'FontSize',12)
% saveas(gcf,'./out/mpt_graph_6.png')

% Figure 7
% f7 = figure('visible', 'off')
% bar(pwgt1','stacked')
% legend(tech_projs_df.Name)
% set(gca,'FontSize',14)
% grid on
% ylabel('Portfolio Weights (fractions) - x_i')
% xlabel('Portfolio #')
% set(gca,'FontSize',14)
% saveas(gcf,'./out/mpt_graph_7.png')
writematrix(pwgt1, './out/pwgt1.txt')